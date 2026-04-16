import { useEffect, useRef, useState } from "react";

type ChatItem = { id: string; sender: string; content: string };

export const Chat = () => {
  const userName = localStorage.getItem("userName");
  const [messages, setMessages] = useState<ChatItem[]>([]);
  const [content, setContent] = useState("");
  const hasStarted = useRef(false);

  useEffect(() => {
    if (hasStarted.current) return;
    hasStarted.current = true;
    const startMessage: ChatItem = {
      id: Date.now().toString(),
      sender: "Serenity",
      content: `Hey ${userName}! Wie geht es dir heute?`,
    };
    setMessages((prev) => [...prev, startMessage]);
  }, []);

  const handleChat = (event) => {
    event.preventDefault();
    setMessages((prev) => [
      ...prev,
      { id: Date.now().toString(), sender: userName, content: content },
    ]);
    setContent("");
  };

  return (
    <main>
      <p>Das ist der Chat von {userName} und Serenity!</p>
      <ul>
        {messages?.map((message) => (
          <li key={message.id}>
            <div
              className={message.sender == userName ? "user-chat" : "ki-chat"}
            >
              {message.content}{" "}
            </div>
          </li>
        ))}
      </ul>
      <form onSubmit={handleChat}>
        <div>
          <label htmlFor="content"> User Message</label>
          <textarea
            name="content"
            id="content"
            value={content}
            onChange={(event) => setContent(event.target.value)}
          ></textarea>
          <button type="submit">☑️</button>
        </div>
      </form>
    </main>
  );
};
