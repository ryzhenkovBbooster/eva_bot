

##                                    1.Администратор курса новичка (АКН) отправляет сообщение в чат ##
def start_message(name, date):

    return f"""Добрый день, @{name}! Рады приветствовать вас в нашей команде! Меня зовут Ева, я - телеграм бот, и буду помогать вам адаптироваться на тестовом периоде. Также хотела бы представить вам Дениса Кравчук @DenKravchuk - специалиста по адаптации, который также будет подключаться для ответов на вопросы, если они у вас возникнут. Стандартное время работы в компании с 9:00 до 18:00 по часовому поясу UTC+3 (Турция, Мадагаскар). Мне передали информацию, что {date} вы готовы приступить, верно?
Ответьте мне на это сообщение 'принято', и мы начнем работать вместе!
"""


def info_message(name):
    return f"""Также я хотела бы отметить, что уведомления в чатах нашей компании выключены, поэтому, чтобы я или Денис могли оперативно реагировать на ваши сообщения, пожалуйста, пишите через @логин в тексте сообщения или используйте функцию "ответить". """


##                                     5.  АКН подготавливает файл с практическими заданиями  для стажера:
def create_practical_tasks(fullname, link):
    return f"""Привет, сотрудник {fullname} вышел на тестовый период, в течении дня он пройдет первый этап курса адаптации, далее во втором этапе ему нужно будет выполнить практические задания, которые покажут его квалификацию. Заполни, пожалуйста, поля “Задание” и “Крайний срок”, они должны быть рассчитаны на 3 дня.  Задачи должны быть составлены так, чтобы показать подходит ли нам этот кандидат. После заполнения должны быть прописаны задачи, время на выполнение задачи и дедлайн выполнения
    {link}"""



##                                      2.Создание адреса электронной почты


def generate_mail(login, passwd):
    return f"""Войдите в вашу корпоративную почту https://www.google.com/intl/ru/gmail/about/ 
Логин: {login}
Пароль: {passwd}
После входа, смените пароль и сообщите о входе в почту ответным сообщением “Почта создана” в данном чате.
"""



def reg_to_skill_up():
    return """Для первичной адаптации в нашей компании мы используем платформу Skill-up. Доступ на платформу был отправлен вам на почту. В разделе "Обучение" вы найдете Курс новичка, который поможет вам освоить основные правила компании, определит ваши компетенции и поможет подготовить ваш компьютер к полноценной работе у нас. Курс необходимо пройти в течении 5 дней, поэтому можете приступать к прохождению!"""

##                                  10. АКН выдает доступ к практическим заданиям сотруднику


def access_to_practical_task(link, manager):
    return f"Направляю ссылку на практические задания. У вас есть 3 рабочих дня на их выполнение." \
           " Пожалуйста, уделите всё внимание заданиям, демонстрируя свою компетентность и профессионализм." \
           " По всем вопросам, связанным с практическим задачам обращайтесь к вашему руководителю в этом чате" \
           f" через https://t.me/{manager}. После выполнения каждого задания, прикрепляйте ссылку на него в столбец 'Отчет'." \
           f" Удачи в выполнении!\n{link}"


##                                  13. АКН запрашивает ОС у руководителя, можно ли переводить сотрудника на ИС

def last_stage(name):
    return f"Поздравляю, {name}, практические задачи успешно приняты руководителем" \
           " и можно приступать к третьему этапу Курса новичка!"

##                                  15. Выдача рабочей почты сотруднику

def rename_email_static(name, additional_email, oldEmail, username):
    return f"""{name}, привет! Я переименовала вашу почту на должностную и открыла доступы. Теперь вам доступны все файле вашего департамента на Google Диске!
Новая почта - {additional_email}, пароль остался прежний.
Предыдущая почта, "{oldEmail}", сохранена в вашем аккаунте и связана с новым адресом. Важно помнить, что все регистрации в сервисах по-прежнему должны осуществляться через "{oldEmail}". И будущие регистрации в сервисах компании также следует создавать с использованием "{oldEmail}".
Если возникнут трудности с доступом или потребуется техническая помощь, не стесняйтесь обращаться к @{username}, он всегда готов помочь вам!
"""


##                                  16.  После сообщения стажера о том, что п. 1 и 2 по уроку LastPass выполнены

def create_lastpass_folder():
    return "Добрый день, вам на почту должно прийти письмо от LastPass." \
           " В тексте письма будет ссылка с папкой доступов, в которую вам необходимо будет сохранять ваши пароли." \
           " Перейдите по ссылке и переместите в папку карточки со всеми корпоративными доступами, которые уже были вами созданы"


##                                    17.Создание личной папки сотрудника на гугл диске

def create_folder_on_drive(link):
    return f"Вот ссылка на вашу рабочую папку - {link} "\
            "В ней необходимо создавать и хранить все рабочие файлы"

##                                   20. АКН проверяет, чтобы все задания в Skill-up были выполнены

def finaly_course_june():
    return "Поздравляю, вы успешно прошли тестовый период и переходите на испытательный срок!" \
           " Я также буду курировать вас на этапе испытательного срока, поэтому по вопросу обучения," \
           " регламентов и в целом адаптации на испытательном сроке, можете смело обращаться ко мне," \
           " в по рабочим задачам - к руководителю @!"


def message_from_given_practical_task(june: str, manager: str, link: str ):
    return f'{june}, направляю ссылку на [практические задания]({link}).' \
           ' У вас есть 3 рабочих дня на их выполнение.' \
           ' Пожалуйста, уделите всё внимание заданиям,' \
           ' демонстрируя свою компетентность и профессионализм. По всем вопросам, связанным с' \
           f' практическим задачам обращайтесь к вашему руководителю в этом чате через @{manager}.' \
           ' После выполнения каждого задания, прикрепляйте ссылку на него в столбец "Отчет". Удачи в выполнении!'


def completed_skillup(june:str, manager: str ):
    return f'@{june} Поздравляю, вы успешно прошли тестовый период и переходите на испытательный' \
           ' срок! Я также буду курировать вас на этапе испытательного срока, поэтому' \
           ' по вопросу обучения, регламентов и в целом адаптации на испытательном сроке,' \
           f' можете смело обращаться к нему, в по рабочим задачам - к руководителю @{manager}!'


def send_to_manager_ipo(link: str):
    return f'Привет, в [ИПО сотрудника]({link}) В ЛИСТЕ ИС необходимо внести рабочие задачи на период ИС' \
           ' для нового сотрудника и указать срок выполнения задач (дедлайны).' \
           ' ИПО необходимо заполнить в течении 1 дня. Сообщи, плз, когда ИПО будет готов,' \
           ' я перепроверю. Спасибо.'


def send_info_about_photo(june: str):
    return {
        'first': f'@{june}, давайте сделаем вам корпоративную подпись в электронном ящике.'
                 ' Пришлите, пожалуйста, свое фото анфас, где хорошо и четко видно лицо и плечи,'
                 ' а фон однотонный (подойдет даже селфи на фоне нейтральной стены;',
        'second': f'@{june}, направляю [инструкцию по добавлению подписи](https://docs.google.com/document/d/15GYIfQmHYXblGcZEBl372Puwux8bG5pn43_vF7onFPA/edit#heading=h.1etqrc9hq5vh) в электронную почту'
                  f' и шаблон вашей подписи. После того, как добавите подпись и настроите отправку писем'
                  f' с псевдонима, пришлите, пожалуйста, тестовое письмо мне на почту d.kravchuk@bbooster.online.',

        "third": f'@{june}, раз в неделю у нас проходит общая встреча сотрудников компании,'
            f' на которой каждый департамент делится достижениями прошлой недели и планами на следующую неделю.'
            f' Также на встрече знакомимся с новыми сотрудниками, поэтому пришлите,'
            f' пожалуйста, свое любимое фото и напишите свой девиз, которому вы следуете по жизни.'
            f' Это поможет нам ближе познакомиться с вами и представить вас коллегам!'
    }


def drop_ipo(june: str, sheet_ipo: str, skillup: str, manager: str):
    return f'@{june}, для более эффективной адаптации каждого нового специалиста мы разрабатываем' \
           f' индивидуальную программу обучения (ИПО), которая включает в себя рабочие задачи,' \
           f' связанные с вашей должностью, а также обучающие материалы,  с которыми необходимо ознакомиться' \
           f' в течение испытательного срока. Рабочие задачи вы найдете по [ссылке]({sheet_ipo}),' \
           f' курировать вас по ним будет прямой руководитель @{manager}. Обучающие материалы' \
           f' мы назвали курсом “Ориентация”, его вы найдете по [ссылке]({skillup}) и курировать вас' \
           f' по ним буду я. С помощью курса вы глубже познакомитесь с основными инструментами' \
           f' и процессами работы в компании. Приступать к обучению уже можете сегодня! Если возникнут сложности или вопросы - смело обращайтесь, я на связи!'

def send_feedback_form():
    return """Для нас очень важно постоянно улучшать наш процесс адаптации, чтобы он был максимально полезным для всех новых сотрудников. В связи с этим мы подготовили небольшую анкету, и будем признательны, если вы сможете уделить немного времени для её заполнения. Заполнить её можно по [ссылке](https://docs.google.com/forms/d/e/1FAIpQLSciyFHIoQJqLFCoqm7fE1nMuca70NYskNCTT-RtUbZCfuP1Mg/viewform) ."""

def send_table_from_manager(june: str, link: str):
    return f'Привет, @{june}, стажер успешно завершил Курс новичка и перешел на ИС.' \
           ' Сегодня я проведу координацию с сотрудником по задачам "Ориентация"' \
           ' в ИПО. Пожалуйста, скоординируйся сегодня с сотрудником для разъяснения' \
           ' рабочих задач.' \
           ' Напоминаю, что все рабочие задачи должны быть приняты руководителем,' \
           ' поэтому, когда ты принимаешь задачу, не забудь поставить отметку' \
           ' "Задача принята". Это поможет мне следить за прогрессом прохождения' \
           ' ИС сотрудником. Также, ссылка на таблицу оценки стажера доступна' \
           f' по [ссылке]({link}). Пожалуйста, каждую неделю вноси данные в таблицу.'


def invate_to_meeting_is(june):
    return f'@{june} Также, для вашей успешной адаптации в компании мы' \
           f' проводим еженедельные встречи сотрудников на испытательном сроке.' \
           f' Эти встречи проходят каждый четверг в 16:30 по часовому поясу' \
           f' UTC+3. Вот ссылка чата сотрудников https://t.me/+OwvCPo0isDMyZDdk, в течении дня я добавлю эту встречу в календарь. ' \
           f' Что касается обсуждения ваших задач на период испытательного' \
           f' срока, мы будем продолжать вести коммуникацию в этом чате.' \
           f' Не стесняйтесь обращаться с вопросами, мы всегда готовы вам' \
           f' помочь'


def invate_to_learn_users(june):
    return f'@{june}, добавляю вас в канал обучения сотрудников' \
           ' Маркетинговой Компании Business Booster.' \
           ' Здесь мы делимся новостями о новых книгах и материалах' \
           ' в нашей онлайн библиотеке, а также публикуем результаты' \
           ' образовательных игр и соревнований между нашими департаментами!'



def finaly_is_from_chat_with_user(june):
    return f"""@{june}, хочу сообщить об успешном завершение испытательного срока, поздравляю вас  с официальным вступлением в должность! Мы рады видеть вас в нашей команде! 🤗
Надеемся ваше развитие в нашей компании будет таким же динамичным и продуктивным!
@tg_sector Данный чат можно архивировать, он потерял свою актуальность, далее сотрудник будет общаться в своих рабочих чатах."""


def finaly_is_from_chat_is(june):
    return f'@{june} сегодня успешно завершил испытательный срок!' \
           ' 🙌🙌🙌 Поздравляем его с официальным вступлением в должность' \
           ' и торжественно убираем из данного чата😊, так как он/она теперь будет' \
           ' посещать другие собрания 💪 Желаем вам успеха и развития у нас в компании!'