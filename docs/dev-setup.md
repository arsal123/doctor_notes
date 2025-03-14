# Dev Setup

## Installation

> Using `asdf` or another Python version manager? Jump to Step 6.

### 1. Install `pyenv` (Skip if using `asdf`)

```sh
curl https://pyenv.run | bash
```

### 2. Configure `pyenv` (macOS/Linux)

Add this to your ~/.zshrc or ~/.bashrc:

```sh
export PATH="$HOME/.pyenv/bin:$PATH"
eval "$(pyenv init --path)"
eval "$(pyenv virtualenv-init -)"
```

Reload the shell:

```sh
exec $SHELL
```

### 3. Install Python 3.10.12

```sh
pyenv install 3.10.12
```

### 4. Set Python version for the project

```sh
cd /path/to/doctor-notes  # Navigate to the project root
pyenv local 3.10.12
```

### 5. Create & activate a virtual environment

```sh
pyenv virtualenv 3.10.12 doctor-notes-env
pyenv activate doctor-notes-env
```

### 6. Install dependencies

```sh
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
pip install -r broker/requirements.txt
pip install -r agents/stt_processor/requirements.txt
pip install -r scripts/requirements.txt
```

Verify installation:

```sh
python --version  # Should output Python 3.10.12
which python  # Should point to .pyenv or .venv
```

---

## Startup

### 1. Start RabbitMQ (Docker)

```sh
docker run -d --name mms-rabbitmq \
  -p 5672:5672 -p 15672:15672 \
  -e RABBITMQ_DEFAULT_USER=admin \
  -e RABBITMQ_DEFAULT_PASS=admin \
  rabbitmq:management
```

Verify:

```sh
docker ps | grep rabbitmq
```

If RabbitMQ was already running:

```sh
docker restart mms-rabbitmq
```

---

### 2. Start the Agents

Run each in a separate terminal tab:

Consultation Orchestrator:

```sh
python -m agents.consultation_orchestrator.consultation_orchestrator_agent
```

STT (Speech-to-Text) Agent:

```sh
python -m agents.stt_processor.stt_agent
```

Notes Generator:

```sh
python -m agents.notes_generator.notes_agent
```

General Medicine NLP Agent:

```sh
python -m agents.specialized_nlp_processors.general_medicine.nlp_gm_agent
```

Mental Health NLP Agent:

```sh
python -m agents.specialized_nlp_processors.mental_health.nlp_mh_agent
```

Nutrition NLP Agent: _(Previously mislabeled as Mental Health)_

```sh
python -m agents.specialized_nlp_processors.nutrition.nlp_nutrition_agent
```

Check if all agents are running:

```sh
ps aux | grep python
```

---

### 3. Send a Test Request

```sh
PYTHONPATH=$(pwd) python scripts/test_stt_send.py
```

Expected Output:

- The STT agent should receive and process the message.
- Logs should indicate that `triggers_all_agents.wav` was processed.

---

## Troubleshooting

Clear the RabbitMQ queue (if stuck messages are causing issues):

```sh
docker exec -it mms-rabbitmq rabbitmqctl purge_queue stt_processor_queue
```

Check RabbitMQ logs:

```sh
docker logs mms-rabbitmq --tail 50
```

Restart all services:

```sh
docker restart mms-rabbitmq
```

Then restart agents in order.

docker run --name medical_notes_db \
    -e POSTGRES_USER=postgres \
    -e POSTGRES_PASSWORD=postgres \
    -e POSTGRES_DB=medical_notes \
    -p 5432:5432 \
    -v pgdata:/var/lib/postgresql/data \
    -d postgres:15

docker exec -it medical_notes_db psql -U postgres -d medical_notes

CREATE TABLE notes (
    id SERIAL PRIMARY KEY,
    patient_id UUID NOT NULL,
    doctor_id UUID NOT NULL,
    transcription TEXT NOT NULL,
    transcription_summary TEXT NOT NULL,  -- New column
    analysis_summary JSONB NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(patient_id, doctor_id)
);








