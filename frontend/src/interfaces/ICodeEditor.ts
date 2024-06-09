export default interface ICodeEditor {
    language: string;
    defaultValue: string;
    onChange: (newValue: string) => void;
  }