import Editor from "@monaco-editor/react";

interface CodeEditorProps {
  value: string;
  language: string;
  onChange: (value: string) => void;
}

export function CodeEditor({
  value,
  language,
  onChange,
}: CodeEditorProps) {
  return (
    <div className="overflow-hidden rounded-2xl border border-border">
      <Editor
        height="600px"
        theme="vs-dark"
        language={language}
        value={value}
        onChange={(nextValue) =>
          onChange(nextValue ?? "")
        }
        options={{
          minimap: {
            enabled: false,
          },
          fontSize: 14,
          automaticLayout: true,
        }}
      />
    </div>
  );
}