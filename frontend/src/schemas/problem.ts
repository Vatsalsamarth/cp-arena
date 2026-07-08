import { z } from "zod";

export const problemSchema = z.object({
  title: z
    .string()
    .min(3)
    .max(200),

  slug: z
    .string()
    .min(3),

  statement: z
    .string()
    .min(10),

  difficulty: z
    .string()
    .regex(/^\d+$/, "Difficulty must be a number"),

  tags: z
    .string()
    .optional(),
});

export type ProblemFormData =
  z.infer<typeof problemSchema>;