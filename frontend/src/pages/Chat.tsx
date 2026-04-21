import { useEffect, useRef, useState } from "react";
import { api } from "../api/axios";

type ChatItem = { id: string; role: string; content: string };

export const Chat = () => {
  const userName = localStorage.getItem("userName");
  const [messages, setMessages] = useState<ChatItem[]>([]);
  const [content, setContent] = useState("");
  const [isWaiting, setIsWaiting] = useState(false);
  const hasStarted = useRef(false);

  useEffect(() => {
    if (hasStarted.current) return;
    hasStarted.current = true;
    const startMessage: ChatItem = {
      id: Date.now().toString(),
      role: "assistant",
      content: `Hey ${userName}! Ich bin Serenity, dein persönlicher Coach. Wie geht es dir heute?`,
    };
    setMessages((prev) => [...prev, startMessage]);
  }, []);

  const handleChat = (event) => {
    setIsWaiting(true);
    event.preventDefault();
    if (!content.trim()) return;
    const newMessage = {
        id: Date.now().toString(),
        role: "user",
        content: content,
      },
      updatedMessages = [...messages, newMessage];
    setMessages(updatedMessages);
    setContent("");
    send_data(updatedMessages);
  };

  const send_data = async (messages: ChatItem[]) => {
    if (messages.length <= 1) return;
    try {
      const response = await api.post("/chat", messages);
      console.log("Erfolg:", response.data);
      alert("Juhuu das hat geklappt");

      if (response.data && response.data.content) {
        const aiMessage = { ...response.data, id: Date.now().toString() };
        setMessages((prev) => [...prev, aiMessage]);
      } else {
        console.error("Error: The response from the server is incomplete");
        alert("Serenity ist gerade sprachlos. Bitte versuche es nocheinmal.");
      }
      //navigate("/chat");
    } catch (error) {
      console.error(error);
      alert("Da ist etwas schief gelaufen.");
    } finally {
      setIsWaiting(false);
    }
  };

  return (
    <main>
      <p>Das ist der Chat von {userName} und Serenity!</p>
      <ul>
        {messages?.map((message) => (
          <li key={message.id}>
            <div className={message.role == "user" ? "user-chat" : "ki-chat"}>
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
          <button type="submit" disabled={isWaiting ? true : false}>
            ☑️
          </button>
        </div>
      </form>
    </main>
  );
};
