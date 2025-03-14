declare module "react-simple-chatbot" {
    import * as React from "react";
  
    export interface Step {
      id: string;
      message?: string;
      user?: boolean;
      trigger?: string;
      options?: { value: string; label: string; trigger: string }[];
      component?: React.ReactNode;
      waitAction?: boolean;
    }
  
    export interface ChatBotProps {
      steps: Step[];
      floating?: boolean;
    }
  
    export default class ChatBot extends React.Component<ChatBotProps, {}> {}
  }
  