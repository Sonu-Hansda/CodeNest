type Language = "python" | "c" | "cpp";

export default interface LanguageToggleProps {
  onChange: (language: Language) => void;
}