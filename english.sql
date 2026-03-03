-- Слово дня
INSERT INTO words (word, translation, example) VALUES
('Resilience', 'Стойкость, жизнестойкость', 'Her resilience helped her overcome the crisis.'),
('Inspiration', 'Вдохновение', 'Nature is a great source of inspiration for many artists.'),
('Ambiguous', 'Двусмысленный, неопределенный', 'The ending of the movie was quite ambiguous.'),
('Procrastinate', 'Откладывать на потом', 'I tend to procrastinate when I have a difficult task.'),
('Eloquence', 'Красноречие', 'The speaker impressed everyone with his eloquence.'),
('Exacerbate', 'Обострять, ухудшать', 'The new law only exacerbated the problem.'),
('Meticulous', 'Тщательный, дотошный', 'She is meticulous about keeping her room clean.'),
('Benevolent', 'Доброжелательный', 'A benevolent smile lit up his face.'),
('Frugal', 'Бережливый, экономный', 'He is frugal with his money but generous with his time.'),
('Authentic', 'Подлинный, настоящий', 'The restaurant serves authentic Italian food.');

--Идиома 
INSERT INTO idioms (phrase, translation, example) VALUES
('To break the ice', 'Растопить лед (начать общение)', 'A joke is a good way to break the ice.'),
('Piece of cake', 'Проще простого', 'The exam was a piece of cake for her.'),
('Under the weather', 'Плохо себя чувствовать', 'I’m feeling a bit under the weather today.'),
('Bite the bullet', 'Стиснуть зубы (принять трудное решение)', 'I decided to bite the bullet and go to the dentist.'),
('Call it a day', 'Закончить на сегодня', 'We’ve been working for 10 hours, let’s call it a day.'),
('Break a leg', 'Ни пуха, ни пера (Удачи)', 'Break a leg on your performance tonight!'),
('Cost an arm and a leg', 'Стоить очень дорого', 'This new car cost me an arm and a leg.'),
('Hit the nail on the head', 'Попасть прямо в точку', 'You hit the nail on the head with that suggestion.'),
('Let the cat out of the bag', 'Проболтаться (выдать секрет)', 'Who let the cat out of the bag about the surprise party?'),
('Burn the midnight oil', 'Работать допоздна', 'I have to burn the midnight oil to finish the project.');

-- Тесты по уровням
-- Формат options: Вариант1,Вариант2,Вариант3,Вариант4 (разделитель - запятая)
INSERT INTO test_questions (level, question_text, options, correct_option) VALUES
-- Уровень A1-A2
('A1', 'I ___ a student.', 'am,is,are,be', 0),
('A1', 'She ___ two brothers.', 'has,have,having,had', 0),
('A2', 'Where ___ you go yesterday?', 'do,did,does,done', 1),
('A2', 'I have never ___ to London.', 'be,was,been,being', 2),
('A2', 'This book is ___ than that one.', 'good,better,best,gooder', 1),

-- Уровень B1-B2
('B1', 'If I ___ you, I would take that job.', 'am,was,were,be', 2),
('B1', 'I look forward to ___ you.', 'see,saw,seen,seeing', 3),
('B2', 'Hardly ___ the office when it started raining.', 'I left,had I left,I had left,did I leave', 1),
('B2', 'You ___ better see a doctor.', 'should,would,had,ought', 2),
('B2', 'She suggested ___ to the cinema.', 'go,to go,going,goes', 2);