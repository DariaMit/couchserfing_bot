import pymysql
import cryptography
import well_another.config as config





class Database:
    def __init__(self, db_file):
        self.connection = pymysql.connect(host="localhost",
                                          user=config.db_user,
                                          password=config.db_password,
                                          db=db_file,
                                          )


    def add_all_for_registration(self, user_id_tg, link_VK, name, is_host, lang, bdate, username_TG):
        print(user_id_tg)
        with self.connection.cursor() as cur:
            cur.execute(f"INSERT INTO all_users (user_id_TG) VALUE ({user_id_tg})")
            cur.execute(f"""UPDATE all_users SET 
            name = '{name}', 
            user_id_TG = '{user_id_tg}',
            link_VK = '{link_VK}',
            is_host = '{is_host}',   
            language = '{lang}',
            bdate = '{bdate}',
            username_TG = '{username_TG}' 
            WHERE user_id_TG = {user_id_tg}""")
            self.connection.commit()
            print('регистрация есть')


    def user_exists(self, user_id):
        with self.connection.cursor() as cur:
            result = cur.execute(f"SELECT * FROM all_users WHERE user_id_TG = {user_id}")
            return bool(result)

    def get_lang(self, user_id):
        with self.connection.cursor() as cur:
            cur.execute(f"SELECT language FROM all_users WHERE user_id_TG = {user_id}")
            return cur.fetchone()[0]


    def get_TG_id(self, id_db):
        with self.connection.cursor() as cur:
            cur.execute(f"SELECT user_id_TG FROM all_users WHERE id = {id_db}")
            return cur.fetchone()[0]


    def get_host_info(self, user_id):
        with self.connection.cursor() as cur:
            cur.execute(f"SELECT link_VK, name FROM all_users WHERE user_id_TG = '{user_id}'")
            id_and_name = cur.fetchone()
            return id_and_name


    def leave_review(self, host_id_db, guest_id, review, date, mark):
        with self.connection.cursor() as cur:
            cur.execute("SELECT id FROM all_users WHERE user_id_TG = %(guest_id)s",
                        {'guest_id': guest_id})
            guest_id_db = cur.fetchone()[0]
            cur.execute("""INSERT INTO reviews (host_id, guest_id, review, date, mark) 
                        VALUES (%(host_id_db)s, %(guest_id_db)s, %(review)s, %(date)s, %(mark)s)""",
                        {'host_id_db': host_id_db, 'guest_id_db': guest_id_db,
                         'review': review, 'date': date, 'mark': mark})
            self.connection.commit()


#не работает((((((
    def get_host_for_review(self, column, link):
        print(column)
        print(link)
        print(f"SELECT id FROM all_users WHERE {column} = {link}")
        with self.connection.cursor() as cur:
            res = cur.execute(f"SELECT id FROM all_users WHERE {column} = '{link}'")
            print('res')
            print(res)
            cur.execute(f"SELECT id FROM all_users WHERE {column} = '{link}'")
            if bool(res):
                id = cur.fetchone()[0]
                print('id из бд функции')
                print(id)
                return id
            else:
                print('а хули нет')
                return False




    # def get_host_for_review(self, column, link):
    #     print(column)
    #     print(link)
    #     with self.connection.cursor() as cur:
    #         res = cur.execute(f"SELECT id FROM all_users WHERE %(column)s = %(link)s",
    #                           {'column': column, 'link': link})
    #         print('res')
    #         print(res)
    #         cur.execute("SELECT id FROM all_users WHERE %(column)s = %(link)s",
    #                     {'column': column, '"link"': link})
    #         id = cur.fetchone()[0]
    #         print('id из бд функции')
    #         print(id)
    #         if bool(res):
    #             id = cur.fetchone()[0]
    #             print('id из бд функции')
    #             print(id)
    #             return id
    #         else:
    #             print('а хули нет')
    #             return False

    def get_host_by_city(self, city):
        '''Возвращает кортеж из всех объявлений в искомом городеб содержащий айди, имя и текст объявления'''

        response = []
        with self.connection.cursor() as cur:
            result = cur.execute("SELECT invitation_text, host_id FROM host_invitations WHERE city = %(city)s",
                                 {'city': city})
            if bool(result):
                cur.execute("SELECT invitation_text, host_id FROM host_invitations WHERE city = %(city)s",
                            {'city': city})
                text_and_id = cur.fetchall()
                invitation_texts = list(map(lambda x: x[0], text_and_id))
                host_ids_db = list(map(lambda x: x[1], text_and_id))
                names = []
                for id in host_ids_db:
                    cur.execute("SELECT name FROM all_users WHERE id = %(id)s",
                                {'id': id})
                    host_name = cur.fetchone()[0]
                    names.append(host_name)
                for id, text, name in zip(host_ids_db, invitation_texts, names):
                    response.append((id, name, text))
                return response
            else:
                return 'В этом городе нет доступных хостов'

    def get_host_reviews(self, id):
        with self.connection.cursor() as cur:
            cur.execute("SELECT review FROM reviews WHERE host_id = %(id)s",
                        {'id': id})
            res = cur.fetchmany(5)
        return res

    def find_host_id(self, id):
        with self.connection.cursor() as cur:
            cur.execute("SELECT user_id_TG FROM all_users WHERE id = %(id)s",
                        {'id': id})
            host_id_TG = cur.fetchone()
            return host_id_TG[0]


    def set_host_invitation(self, user_id, text, city):
        with self.connection.cursor() as cur:
            cur.execute("SELECT id FROM all_users WHERE user_id_TG = %(user_id)s",
                        {'user_id': user_id})
            id = cur.fetchone()[0]
            cur.execute("""INSERT INTO host_invitations (host_id, city, invitation_text) 
                            VALUES (%(id)s, %(city)s, %(text)s)""",
                        {'id': id, 'city': city, 'text': text})
            self.connection.commit()



    def reset_host_invitation(self, user_id, text, city):
        with self.connection.cursor() as cur:
            cur.execute(f"""UPDATE host_invitations SET
             city = {city},
             invitation_text = {text}
             WHERE host_id = {user_id}
             """)
            self.connection.commit()

    #шо-то не работает(((((((((
    # def reset_host_invitation(self, user_id, text, city):
    #     print('мы тут')
    #     with self.connection.cursor() as cur:
    #         cur.execute("""UPDATE host_invitations SET
    #          city = %(city)s,
    #          invitation_text = %(text)s
    #          WHERE host_id = %(user_id)s
    #          """, {'city': city, 'text': text, 'user_id': user_id})
    #         self.connection.commit()
    #     print('теперь тут')


    def user_invitation_exists(self, user_id):
        with self.connection.cursor() as cur:
            cur.execute("SELECT id FROM all_users WHERE user_id_TG = %(user_id)s",
                        {'user_id': user_id})
            id = cur.fetchone()[0]
            result = cur.execute(f"SELECT * FROM host_invitations WHERE host_id = %(id)s",
                                 {'id': id})
            return bool(result)

    def check_city_eng(self, city):
        with self.connection.cursor() as cur:
            cur.execute("SELECT code_number FROM cities_numbers WHERE city_eng = %(city)s",
                        {'city': city})
            if cur.fetchone():
                return cur.fetchone()[0]
            else:
                cur.execute("""INSERT INTO cities_numbers (city_eng) 
                            VALUES (%(city)s)""",
                            {'city': city})

