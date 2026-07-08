import { z } from "zod";

export const problemSchema = z.object({
  title: z
    .string()
    .min(3)
    .max(200),

  slug: z
    .string()
    .min(3),

  description: z
    .string()
    .min(10),

  difficulty: z.enum([
    "easy",
    "medium",
    "hard",
  ]),

  tags: z
    .string()
    .optional(),
});

export type ProblemFormData =
  z.infer<typeof problemSchema>;