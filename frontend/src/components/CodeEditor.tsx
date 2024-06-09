import MonacoEditor from "react-monaco-editor";
import ICodeEditor from "../interfaces/ICodeEditor";

export default function CodeEditor({
    language,
    defaultValue,
    onChange,
  }:ICodeEditor){
    const options = {
        selectOnLineNumbers: true,
      };
    return (
        <MonacoEditor
        width="100%"
        height="500"
        language={language}
        theme="vs-dark"
        value={defaultValue}
        options={options}
        onChange={onChange}
      />
    );
}