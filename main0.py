from auto_grader_ai import Auto_Grader_AI

rubric: str = 'Creativity: High, Medium, Low'
submission: str = 'My name is Jacob, I am a sophamore at WPI. I am a computer science major. I am interested in machine learning and artificial inteligence. I am currently working on a project that uses machine learning to create artificial inteligence. I think I would be great for this pogram!'

AI = Auto_Grader_AI(rubric)

grade = AI.grade(submission)

print(grade)