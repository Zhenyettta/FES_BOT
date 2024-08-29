from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import CallbackContext, CommandHandler, ConversationHandler, MessageHandler, filters

from bot.handlers.start import fresh_start
from bot.utils.fields import *
from bot.utils.utils import generic_reply, go_home, unlucky

BACK = 'Назад'
HOME = 'На головну'
LEARNING_PROCESS, USEFUL_INFO = range(2)
DEAN_RESPONSIBILITIES, DEPUTY_DEAN_RESPONSIBILITIES, DEPARTMENT_RESPONSIBILITIES, INDIVIDUAL_PLAN = range(3, 7)
WHAT_IS_IT, WHAT_TO_DO, EXPULSION = range(7, 10)
ACADEMIC_LEAVE, EXCLUSION, RENEWAL = range(12, 15)


# Learning Process Handlers
async def learning_process(update: Update, context: CallbackContext) -> int:
    buttons = [['Відповідальність деканату', 'Відповідальність заступника декана'],
               ['Відповідальність кафедр', 'Індивідуальний навчальний план'],
               ['Корисна інформація']]
    return await generic_reply(update, 'Оберіть категорію навчального процесу:', buttons, LEARNING_PROCESS,
                               back_button=True)


async def dean_responsibilities(update: Update, context: CallbackContext) -> int:
    return await generic_reply(update, """-  Складання рейтингів за підсумками заліково-екзаменаційних сесій (протягом 17-20 днів  після завершення сесії)

-  Складання списків на призначення стипендій ((через 17-20 днів  після завершення сесії)

-  Прийом та оформлення заяв на відрахування, поновлення,  академічну відпустку (виключно протягом семестру), переслуховування дисциплін

-  Видача довідок про підтвердження  статусу студента

-  Виписування з нормативних дисциплін при оформленні мобільності

-  Погодження (фінальне, після узгодження з кафедрами) документів на мобільність, змін в програмах мобільності  та оформлення Наказів на мобільність

-  Внесення оцінок після мобільності на основі наданих транскриптів від міжнародного відділу НаУКМА

-  Контроль за ІНП студентів""", [], DEAN_RESPONSIBILITIES, back_button=True, home_button=True, back_home_row=True)


async def deputy_dean_responsibilities(update: Update, context: CallbackContext) -> int:
    return await generic_reply(update, """-  Нарахування годин студентам по корпоративній угоді від факультету;

-  Підготовка характеристики студента для військової кафедри;

-  Робота зі студентами щодо відзнак та іменних стипендій;

-  Інформування студентів щодо конкурсів студентських робіт;

-  Реєстрація звернень у зошиті пропозицій студентів та «скриньці довіри»;

-  Залучення студентів до проведення факультетських заходів;

-  Організація зборів/нарад старост факультету.""", [], DEPUTY_DEAN_RESPONSIBILITIES,
                               back_button=True, home_button=True, back_home_row=True)


async def department_responsibilities(update: Update, context: CallbackContext) -> int:
    return await generic_reply(update, """-  Питання взаємодії з викладачами.

-  Допомога у формуванні Індивідуального плану студента.

-  Узгодження курсів на мобільність.

-  Запис на теми курсових робіт та призначення керівників.

-  Запис на теми кваліфікаційних робіт та призначення керівників.

-  Призначення керівників переддипломної науково-дослідної, педагогічної практики.

-  Допомога в пошуку бази практики. Реєстрація договорів з практики.

-  Виписування з дисциплін під час тижнів корекції при підтвердженні деканатом співпадіння в розкладі. Але після тижнів корекції всі виписування виключно в деканаті (за наявності вагомої причини чому це не було зроблено у визначені терміни через кафедру).""",
                               [], DEPARTMENT_RESPONSIBILITIES,
                               back_button=True, home_button=True, back_home_row=True)


async def individual_plan(update: Update, context: CallbackContext) -> int:
    buttons = [['Що це?', 'Що робити, якщо курс не відбувся?'], ['Виписування з курсів']]
    return await generic_reply(update, 'Індивідуальний навчальний план: оберіть питання:', buttons, INDIVIDUAL_PLAN,
                               back_button=True, home_button=True)


async def what_is_it(update: Update, context: CallbackContext) -> int:
    return await generic_reply(update, """ІНП студента це Перелік навчальних дисциплін які Ви вивчаєте.

Нормативні (обов’язкові) дисципліни автоматично зафіксовані.

Також студент/ка має набрати певну кількість вибіркових курсів професійного спрямування та вільного вибору.

Це фіксується в плані з розподілом по семестрам прослуховування кількістю кредитів та кількістю годин тижневого навантаження.

Запис на курси відбувається через САЗ – систему автоматизованого запису.

Формування, регулярний моніторинг та виконання ІНП – це особиста відповідальність студента!
ВАЖЛИВО! Правильно рахувати всі набрані за час навчання кредити! Недобір навіть в 0,5 кредити призведе до невипуску!""",
                               [], WHAT_IS_IT, back_button=True, home_button=True, back_home_row=True)


async def what_to_do(update: Update, context: CallbackContext) -> int:
    return await generic_reply(update,
                               """Під час тижня корекції потрібно записатись на інший курс, доступний до запису не порушивши норми тижневого навантаження та кількості кредитів.""",
                               [], WHAT_TO_DO, back_button=True,
                               home_button=True, back_home_row=True)


async def expulsion(update: Update, context: CallbackContext) -> int:
    return await generic_reply(update, """Це можна зробити під час тижнів корекції при виникненні співпадіння в розкладі з нормативною дисципліною.
 Деканат має підтвердити таке співпадіння. Для уникнення недобору кредитив студент має дописатись на інший курс!""", [],
                               EXPULSION, back_button=True,
                               home_button=True, back_home_row=True)


# Useful Information Handlers
async def useful_info(update: Update, context: CallbackContext) -> int:
    buttons = [['Академічна відпустка', 'Відрахування'], ['Поновлення', 'Зразки популярних заяв']]
    return await generic_reply(update, 'Оберіть корисну інформацію:', buttons, USEFUL_INFO, home_button=True,
                               back_button=True)


async def academic_leave(update: Update, context: CallbackContext) -> int:
    return await generic_reply(update,
                               'Академічна відпустка: [посилання](https://www.ukma.edu.ua/index.php/about-us/sogodennya/dokumenty-naukma/doc_download/3435-polozhennia-pro-vidrakhuvannia-perevedennia-nadannia-akademichnoi-vidpustky-studentam-v-naukma).',
                               [], ACADEMIC_LEAVE, back_button=True,
                               home_button=True, parse_mode=ParseMode.MARKDOWN)


async def exclusion(update: Update, context: CallbackContext) -> int:
    return await generic_reply(update,
                               """https://www.ukma.edu.ua/index.php/about-us/sogodennya/dokumenty-naukma/doc_download/3435-polozhennia-pro-vidrakhuvannia-perevedennia-nadannia-akademichnoi-vidpustky-studentam-v-naukma""",
                               [], EXCLUSION, back_button=True, home_button=True, back_home_row=True)


async def renewal(update: Update, context: CallbackContext) -> int:
    return await generic_reply(update,
                               """https://www.ukma.edu.ua/index.php/about-us/sogodennya/dokumenty-naukma/doc_download/3435-polozhennia-pro-vidrakhuvannia-perevedennia-nadannia-akademichnoi-vidpustky-studentam-v-naukma""",
                               [], RENEWAL, back_button=True, home_button=True, back_home_row=True)


async def popular_statements(update: Update, context: CallbackContext) -> int:
    return await generic_reply(update, 'Зразки популярних заяв:', [], RENEWAL, back_button=True,
                               home_button=True, back_home_row=True)


# Conversation Handler
learning_process_handler = ConversationHandler(
    entry_points=[MessageHandler(filters.Regex('Навчальний процес'), learning_process)],
    states={
        LEARNING_PROCESS: [
            MessageHandler(filters.Regex('Відповідальність деканату'), dean_responsibilities),
            MessageHandler(filters.Regex('Відповідальність заступника декана'), deputy_dean_responsibilities),
            MessageHandler(filters.Regex('Відповідальність кафедр'), department_responsibilities),
            MessageHandler(filters.Regex('Індивідуальний навчальний план'), individual_plan),
            MessageHandler(filters.Regex('Корисна інформація'), useful_info),
            MessageHandler(filters.Regex(BACK), go_home),
        ],
        DEAN_RESPONSIBILITIES: [
            MessageHandler(filters.Regex(BACK), learning_process),
            MessageHandler(filters.Regex(HOME), go_home),
        ],
        DEPUTY_DEAN_RESPONSIBILITIES: [
            MessageHandler(filters.Regex(BACK), learning_process),
            MessageHandler(filters.Regex(HOME), go_home),
        ],
        DEPARTMENT_RESPONSIBILITIES: [
            MessageHandler(filters.Regex(BACK), learning_process),
            MessageHandler(filters.Regex(HOME), go_home),
        ],
        INDIVIDUAL_PLAN: [
            MessageHandler(filters.Regex('Що це?'), what_is_it),
            MessageHandler(filters.Regex('Що робити, якщо курс не відбувся?'), what_to_do),
            MessageHandler(filters.Regex('Виписування з курсів'), expulsion),
            MessageHandler(filters.Regex(BACK), learning_process),
            MessageHandler(filters.Regex(HOME), go_home),
        ],
        WHAT_IS_IT: [
            MessageHandler(filters.Regex(BACK), individual_plan),
            MessageHandler(filters.Regex(HOME), go_home),
        ],
        WHAT_TO_DO: [
            MessageHandler(filters.Regex(BACK), individual_plan),
            MessageHandler(filters.Regex(HOME), go_home),
        ],
        EXPULSION: [
            MessageHandler(filters.Regex(BACK), individual_plan),
            MessageHandler(filters.Regex(HOME), go_home),
        ],
        USEFUL_INFO: [

            MessageHandler(filters.Regex('Академічна відпустка'), academic_leave),
            MessageHandler(filters.Regex('Відрахування'), exclusion),
            MessageHandler(filters.Regex('Поновлення'), renewal),
            MessageHandler(filters.Regex('Зразки популярних заяв'), popular_statements),
            MessageHandler(filters.Regex(BACK), go_home),
        ],

        ACADEMIC_LEAVE: [
            MessageHandler(filters.Regex(BACK), useful_info),
            MessageHandler(filters.Regex(HOME), go_home),
        ],
        EXCLUSION: [
            MessageHandler(filters.Regex(BACK), useful_info),
            MessageHandler(filters.Regex(HOME), go_home),
        ],
        RENEWAL: [
            MessageHandler(filters.Regex(BACK), useful_info),
            MessageHandler(filters.Regex(HOME), go_home),
        ],
    },
    fallbacks=[CommandHandler('reset', fresh_start), CommandHandler('start', fresh_start),
               MessageHandler(filters.TEXT, unlucky)],
    name='learning-process-handler',
    persistent=True,
)
