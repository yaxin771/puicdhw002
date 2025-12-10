import { useState } from "react";

export default function AIDebateAssistant() {
  const [apiKey, setApiKey] = useState("");
  const [prompt, setPrompt] = useState("");
  const [response, setResponse] = useState("");
  const [loading, setLoading] = useState(false);

  const callAPI = async () => {
    setLoading(true);
    setResponse("");
    try {
      const res = await fetch("https://api.openai.com/v1/chat/completions", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${apiKey}`,
        },
        body: JSON.stringify({
          model: "gpt-4.1",
          messages: [
            { role: "system", content: "你是辯論稿修改助理。" },
            { role: "user", content: prompt },
          ],
          temperature: 0.7,
        }),
      });

      const data = await res.json();
      setResponse(data.choices?.[0]?.message?.content || "無回應");
    } catch (err) {
      setResponse("發生錯誤：" + err.message);
    }
    setLoading(false);
  };

  return (
    <div className="min-h-screen bg-gray-100 p-6 flex justify-center items-start">
      <div className="w-full max-w-3xl bg-white shadow-lg rounded-2xl p-6 space-y-4">
        <h1 className="text-2xl font-bold">AI 辯論助理網頁介面</h1>

        <div className="space-y-2">
          <label className="font-medium">你的 OpenAI API Key：</label>
          <input
            type="password"
            className="w-full p-2 border rounded-lg"
            placeholder="sk-xxxx"
            value={apiKey}
            onChange={(e) => setApiKey(e.target.value)}
          />
        </div>

        <div className="space-y-2">
          <label className="font-medium">輸入辯論稿或請求：</label>
          <textarea
            className="w-full p-3 border rounded-lg h-40"
            placeholder="請輸入要修改的稿子、生成稿子、或任何指令"
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
          />
        </div>

        <button
          className="bg-blue-600 text-white px-4 py-2 rounded-xl shadow hover:bg-blue-700"
          disabled={loading}
          onClick={callAPI}
        >
          {loading ? "生成中..." : "送出"}
        </button>

        <div>
          <h2 className="text-xl font-semibold">AI 回應：</h2>
          <div className="whitespace-pre-wrap bg-gray-50 p-4 rounded-xl border min-h-[120px]">
            {response || "尚無回應"}
          </div>
        </div>
      </div>
    </div>
  );
}
