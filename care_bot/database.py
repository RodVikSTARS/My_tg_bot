import aiosqlite


class DataBase:
    # def __init__(self):
    #     self.create_connection()

    async def create_connection(self):
        self.con = await aiosqlite.connect('care_bot_db.db')
        await self.create_tables()

    async def create_tables(self):
        await self.con.execute('''CREATE TABLE IF NOT EXISTS questions 
                                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                                user_id INTEGER,
                                question TEXT,
                                is_solved BOOLEAN DEFAULT false)''')

        await self.con.execute('''CREATE TABLE IF NOT EXISTS users 
                                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                                user_id INTEGER)''')

    async def add_question(self, user_id: int, question: str):
        async with self.con.execute('''INSERT INTO questions (user_id, question) VALUES(?, ?)''', (user_id, question)):
            await self.con.commit()

    async def get_unsolved_questions(self):
        async with self.con.execute('''SELECT * FROM questions WHERE is_solved = false''') as cur:
            return await cur.fetchall()

    async def get_unsolved_questions_id(self):
        async with self.con.execute('''SELECT id FROM questions WHERE is_solved = false''') as cur:
            return await cur.fetchall()

    async def make_un_to_solved(self, question_id: int):
        async with self.con.execute('''UPDATE questions SET is_solved = true WHERE id = ?''', (question_id,)):
            await self.con.commit()

    async def make_solved_to_un(self, question_id: int):
        async with self.con.execute('''UPDATE questions SET is_solved = false WHERE id = ?''', (question_id,)):
            await self.con.commit()

    async def add_user(self, user_id: int):
        async with self.con.execute('''INSERT INTO users (user_id) VALUES(?)''', (user_id,)):
            await self.con.commit()

    async def get_users(self):
        async with self.con.execute('''SELECT * FROM users''') as cur:
            return await cur.fetchall()



db = DataBase()
