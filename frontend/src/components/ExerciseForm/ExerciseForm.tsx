import { useState } from "react";
import styles from "./ExerciseForm.module.css";

interface ExerciseFormProps {
  handleSubmit(exercise: {
    title: string;
    content: string;
    instructions: string | null;
    media: string | null;
  }): void;
  editExercise?: {
    id?: number;
    title: string;
    content: string;
    instructions: string | null;
    media: string | null;
  };
}

export const ExerciseForm = ({
  handleSubmit,
  editExercise,
}: ExerciseFormProps) => {
  const [title, setTitle] = useState(editExercise?.title ?? "");
  const [content, setContent] = useState(editExercise?.content ?? "");
  const [instructions, setInstructions] = useState(
    editExercise?.instructions ?? "",
  );
  const [media, setMedia] = useState(editExercise?.media ?? "");
  const handleExercise = (event: React.SubmitEvent) => {
    event.preventDefault();
    const exercise = {
      title: title,
      content: content,
      instructions: instructions ? instructions : null,
      media: media ? media : null,
    };
    handleSubmit(exercise);
    setTitle("");
    setContent("");
    setInstructions("");
    setMedia("");
  };
  return (
    <form onSubmit={handleExercise}>
      <div className={styles.inputWrapper}>
        <label htmlFor="title">Titel </label>
        <input
          className={styles.input}
          type="text"
          name="title"
          id="title"
          value={title}
          onChange={(event) => setTitle(event.target.value)}
        />
      </div>
      <div className={styles.inputWrapper}>
        <label htmlFor="content">Beschreibung: </label>
        <textarea
          className={styles.text}
          name="content"
          id="content"
          value={content}
          onChange={(event) => setContent(event.target.value)}
        />
      </div>
      <div className={styles.inputWrapper}>
        <label htmlFor="instructions">Spezielle Anweisungen: </label>
        <textarea
          className={styles.text}
          name="instructions"
          id="instructions"
          value={instructions}
          onChange={(event) => setInstructions(event.target.value)}
        />
      </div>

      <div className={styles.inputWrapper}>
        <label htmlFor="media">Media Link (optional) </label>
        <input
          className={styles.input}
          type="text"
          name="media"
          id="media"
          value={media}
          onChange={(event) => setMedia(event.target.value)}
        />
      </div>
      <button type="submit">Übung speichern</button>
    </form>
  );
};
