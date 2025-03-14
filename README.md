MULTIAGENT DOCTOR NOTES


there are be next agents:
- Speech-to-Text (STT) Processor
- Consultation Orchestrator - Main doctor
- Specialized NLP Processors
- Medical History Agent [out of scope for now]
- FHIR Generator
- UI for Doctor Review
 
Agents should communicate through message broker where it makes sense instead of direct communication.
 
the flow will be 
We have a record of consultation between specialized doctor and patient. This record will be translated to text by Speech-to-Text (STT) Processor and passed to Consultation Orchestrator. 

It decides based on metadata or dynamically by self decision which specific Specialized NLP Processors should we consult. It also decides if we need to request medical history data from Medical History Agent. Then combined information passed to FHIR Generator that generate FHIR post consult documentation and if needed can request additional information from Specialized NLP Processors or Medical History Agent. Then pass it to UI for Doctor Review agent where doctor can review and ask for additional data or details and update docs. Doctor can also manually update docs in Review Agent.
 
It should be an easy way to add new specialized agents without affecting the rest of the system. We should have Agent Directory that dynamically tracks available agents. Agents can register themselves. Then system should query registry to find appropriate agent.
 
If agent provide low confidence data then FHIR Generator can ask agent for verification and highlight this part for Doctor Review agent so it will be highlighted during review. FHIR Generator can also request additional context or verification from doctor.

Specialized NLP Processors can advice to schedule a visit with human specialist.

Project frontend Run instructions:

backend start - 
cd doctor-notes
python server.py
available at http://127.0.0.1:5000/

frontend setup:
cd doctor-review-ui
npm install
npm run dev
available at http://127.0.0.1:5173/