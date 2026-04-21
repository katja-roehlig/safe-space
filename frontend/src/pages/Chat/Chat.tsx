import { useEffect, useRef, useState } from "react";
import { api } from "../../api/axios";
import styles from "./Chat.module.css";

type ChatItem = { id: string; role: string; content: string };

export const Chat = () => {
  const userName = localStorage.getItem("userName");
  const [messages, setMessages] = useState<ChatItem[]>([]);
  const [content, setContent] = useState("");
  const [isWaiting, setIsWaiting] = useState(false);
  const hasStarted = useRef(false);
  const cursorRef = useRef<HTMLInputElement>(null);
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
      console.log("Juhuu, das hat geklappt:", response.data);

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
      cursorRef.current?.focus();
    }
  };

  return (
    <main>
      <ul className={styles.messageList}>
        {messages?.map((message) => (
          <li key={message.id}>
            <div
              className={`${styles.chatBubble}
                ${message.role == "user" ? styles.userChat : styles.kiChat}`}
            >
              {message.content}
            </div>
          </li>
        ))}
      </ul>
      <form onSubmit={handleChat} className={styles.formContainer}>
        <label htmlFor="content" className={styles.label}>
          User Message
        </label>
        <textarea
          className={styles.input}
          name="content"
          id="content"
          value={content}
          onChange={(event) => setContent(event.target.value)}
          placeholder="Schreib etwas ..."
          autoFocus
        ></textarea>
        <button
          type="submit"
          disabled={isWaiting ? true : false}
          className={styles.submitButton}
        >
          ✔️
        </button>
      </form>
    </main>
  );
};
