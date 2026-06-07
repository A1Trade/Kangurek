import { getLessonIndex } from "@/lib/data/lessons";
import { DziennikClient } from "./client";

export default function DziennikPage() {
  const index = getLessonIndex();
  return <DziennikClient index={index} />;
}
