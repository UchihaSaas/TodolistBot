import psycopg2
from config import host, database, password, user
from connect import bot

async def establish_connection():
    return psycopg2.connect(
        host=host,
        database=database,
        user=user,
        password=password
    )

async def check_user(user_id):
    connection = await establish_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT user_id FROM users WHERE user_id = %s", (user_id,))
            result = cursor.fetchone()
            if result is None:
                return "User does not exist."
            else:
                cursor.execute("SELECT user_id, user_name FROM users WHERE user_id = %s", (user_id,))
                result = cursor.fetchone()
                return f"User id: {result[0]}\nUser name: {result[1]}"
    except Exception as ex:
        print("Error:", ex)
        return "An error occurred."
    finally:
        if connection:
            connection.close()

async def add_user(data, user_id):
    connection = await establish_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT user_id, user_name FROM users WHERE user_id = %s", (user_id,))
            result = cursor.fetchone()
            if result is None:
                cursor.execute("""
                    INSERT INTO users (user_id, user_name)
                    VALUES (%s, %s)
                    """, (data['user_id'], data['user_name']))
                connection.commit()
                result = "User added successfully."
                return result
            else:
                result = "User already exists."
                return result
    except Exception as ex:
        print("Ошибка при работе", ex)
        return "An error occurred."
    finally:
        if connection:
            connection.close()
        print("Подключение закончено")

async def rename_user(data):
    connection = await establish_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
            UPDATE users SET user_name = %s 
            WHERE user_id  = %s""",(data['user_name'],data['user_id']))
        connection.commit()
    except Exception as ex:
        print("Ошибка при работе", ex)
        return "An error occurred."
    finally:
        if connection:
            connection.close()
        print("Подключение закончено")

async  def set_task(data):
    connection  = await establish_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                f"INSERT INTO tasks (user_fkid, description) VALUES ({data['user_id']},'{data['task_desctiption']}')")



            connection.commit()
    except Exception as ex:
        print("Ошибка при работе", ex)
        return "An error occurred."
    finally:
        if connection:
            connection.close()
        print("Подключение закончено")

async  def show_todolist(user_id):
    connection = await establish_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT tasks.completed, tasks.task_id, tasks.description FROM tasks WHERE user_fkid = %s",
                           (user_id,))
            result = cursor.fetchall()
        return result
    except Exception as ex:
        print("Ошибка при работе", ex)
        return "An error occurred."
    finally:
        if connection:
            connection.close()
        print("Подключение закончено")

async def edit_completed(data):
    connection = await establish_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("""SELECT completed FROM tasks WHERE tasks.task_id = %s""",(data['edit_task_id'],))
            result = cursor.fetchone
            if result == "false":
                with connection.cursor() as cursor:
                    cursor.execute("""UPDATE tasks SET completed = 'true' WHERE tasks.user_fkid = %s and task_id = %s""",
                                   (data['user_id'], data['edit_task_id']))
                connection.commit()
            else:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """UPDATE tasks SET completed = 'false' WHERE tasks.user_fkid = %s and task_id = %s""",
                        (data['user_id'], data['edit_task_id']))
                connection.commit()

    except Exception as ex:
        print("Ошибка при работе", ex)
        return "An error occurred."
    finally:
        if connection:
            connection.close()
            print("Подключение закончено")

async def edit_description(data):
    connection = await establish_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("""UPDATE tasks SET description = %s WHERE tasks.user_fkid = %s and task_id = %s""",
                           (data['new_desc'],data['user_id'], data['edit_task_id']))
        connection.commit()
    except Exception as ex:
        print("Ошибка при работе", ex)
        return "An error occurred."
    finally:
        if connection:
            connection.close()
            print("Подключение закончено")


async def edit_delete(data):
    connection = await establish_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("""DELETE FROM tasks WHERE task_id = %s""",
                           (data['edit_task_id'],))
        connection.commit()
    except Exception as ex:
        print("Ошибка при работе", ex)
        return "An error occurred."
    finally:
        if connection:
            connection.close()
            print("Подключение закончено")