from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import CallbackContext, CommandHandler, ConversationHandler, MessageHandler, filters

from bot.handlers.start import fresh_start
from bot.utils.utils import generic_reply, go_home, unlucky

BACK = 'Назад'
HOME = 'На головну'
MOBILITY_CATEGORY, MOBILITY_GENERAL, MOBILITY_PROGRAMS, SELF_INITIATED_MOBILITY, DEPARTURE_PROCEDURE, RESULTS_PROCEDURE, FAILED_MOBILITY, APPROVAL = range(
    8)


# Handlers for "Мобільність"
async def mobility(update: Update, context: CallbackContext) -> int:
    buttons = [['Загальна інформація мобільність', 'Програми мобільності'],
               ['Самоініційована мобільність', 'Порядок оформлення від’їзду'],
               ['Порядок оформлення результатів', 'Незарах на мобільності'],
               ['Погодження']]
    return await generic_reply(update, 'Оберіть категорію:', buttons, MOBILITY_CATEGORY, back_button=True)


async def mobility_general(update: Update, context: CallbackContext) -> int:
    text = (
        "Для перегляду положення про мобільність, перейдіть за [посиланням](https://www.ukma.edu.ua/index.php/about-us/sogodennya/dokumenty-naukma/doc_download/3413-polozhennia-pro-poriadok-uchasti-u-prohramakh-vnutrishnoi-i-mizhnarodnoi-akademichnoi-mobilnosti)."
    )
    return await generic_reply(update, text, [], MOBILITY_GENERAL, back_button=True, home_button=True,
                               back_home_row=True,
                               parse_mode=ParseMode.MARKDOWN)


async def mobility_programs(update: Update, context: CallbackContext) -> int:
    text = (
        "Для перегляду інформації про програми мобільності, перейдіть за [посиланням](https://dfc.ukma.edu.ua/going-from-naukma/why-international-experience)."
    )
    return await generic_reply(update, text, [], MOBILITY_PROGRAMS, back_button=True, home_button=True,
                               back_home_row=True,
                               parse_mode=ParseMode.MARKDOWN)

async def approval(update: Update, context: CallbackContext) -> int:
    text = (
        """Відповідальні особи на кафедрах:

1. Кафедра ЕТ​– Бажал Юрій Миколайович, bazhal@ukma.edu.ua

2. Кафедра фінансів:
– для бакалаврів – Слав’юк Наталія Ростиславівна,  n.slaviuk@ukma.edu.ua
– для магістрів ​–  Прімєрова Олена Костянтинівна,  o.primierova@ukma.edu.ua

3. Кафедра МУБ – Пічик Катерина Валеріївна, pichykkv@ukma.edu.ua
 
ВАЖЛИВО! Якщо дисципліна викладається іншою кафедрою/факультетом її потрібно погодити саме на цій кафедрі! Наприклад, курс «Англійська мова»."""
    )
    return await generic_reply(update, text, [], APPROVAL, back_button=True, home_button=True,
                               back_home_row=True,
                               parse_mode=ParseMode.MARKDOWN)


async def self_initiated_mobility(update: Update, context: CallbackContext) -> int:
    text = (
        """Самоініційована мобільність — це мобільність, яку знайшов сам студент. Для погодження цієї мобільності дотримуйтеся наступних інструкцій: 
        
1.	Заповніть [реєстраційну форму](https://forms.office.com/Pages/ResponsePage.aspx?id=Q_7LuAzJ6kuErr5dbYpfUnuidkvbLkpIkb46ooJiACFUQVc5U1M5NDg5OEVMMTBFVFpRQVBKR0NMVy4u), щоб і Ваша кафедра, і деканат, і міжнародний відділ дізналися, що Ви плануєте їхати на мобільність.

2.	Погодьте із завідувачем Вашої випускової кафедри зміст Вашої мобільності, перезарахування вивченого на мобільності, а також можливе перенесення вивчення певних дисциплін, запланованих на семестр мобільності; індивідуальний графік вивчення дисциплін НаУКМА (які неможливо / недоцільно переносити). Для зручності, Ви можете скористатися [формою](https://ukmaedu-my.sharepoint.com/:w:/g/personal/larch_ukma_edu_ua/EaZWy1I9TXhIiuN3SRf6fPgBQ0OTc9TpBeIybE5zNlL7fw?e=cBDFXp) для погодження  

3.	Якщо дисципліна викладається іншою кафедрою її потрібно узгодити з завідувачем відповідної кафедри!

4.	Заповнити онлайн Договір на мобільність та Заяву про перенесення дисциплін, виписування та індивідуальний графік. 

5.	Будь які зміни мають бути погоджені та зафіксовані в договорі протягом 60 днів від початку мобільності

"""
    )
    return await generic_reply(update, text, [], SELF_INITIATED_MOBILITY, back_button=True, home_button=True,
                               back_home_row=True,
                               parse_mode=ParseMode.MARKDOWN)


async def departure_procedure(update: Update, context: CallbackContext) -> int:
    text = (
        """Для оформлення від’їзду на мобільність дотримуйтеся наступних інструкцій:
        
1. Оберіть програму мобільності.

2. Погодьте із завідувачем Вашої випускової кафедри зміст Вашої мобільності, перезарахування вивченого на мобільності, а також можливе перенесення вивчення певних дисциплін, запланованих на семестр мобільності; індивідуальний графік вивчення дисциплін НаУКМА (які неможливо / недоцільно переносити). Для зручності, Ви можете скористатися [формою для погодження](https://ukmaedu-my.sharepoint.com/:w:/g/personal/larch_ukma_edu_ua/EaZWy1I9TXhIiuN3SRf6fPgBQ0OTc9TpBeIybE5zNlL7fw?e=cBDFXp&wdLOR=cB625FE3B-9BBE-4FD6-97DE-9C7D81C36659). 

3. Якщо дисципліна викладається іншою кафедрою, її потрібно узгодити з завідувачем відповідної кафедри.

4. Заповніть онлайн Договір на мобільність та Заяву про перенесення дисциплін, виписування та індивідуальний графік. 

5. Будь-які зміни мають бути погоджені та зафіксовані в договорі протягом 60 днів від початку мобільності.

"""
    )
    return await generic_reply(update, text, [], DEPARTURE_PROCEDURE, back_button=True, home_button=True, back_home_row=True,
                               parse_mode=ParseMode.MARKDOWN)

async def results_procedure(update: Update, context: CallbackContext) -> int:
    text = (
        """Для оформлення і зарахування результатів навчання на мобільності дотримуйтеся наступних інструкцій:
        
1. Транскрипт з оцінками надходить до міжнародного відділу.

2. Співробітники відділу готують супровідний лист з переведенням оцінок університета-партнера у систему оцінок НаУКМА.

3. Ця інформація передається в деканат для перезарахування.

"""
    )
    return await generic_reply(update, text, [], RESULTS_PROCEDURE, back_button=True, home_button=True, back_home_row=True,
                               parse_mode=ParseMode.MARKDOWN)

async def failed_mobility(update: Update, context: CallbackContext) -> int:
    text = (
        """Якщо Ви отримали незадовільну оцінку на мобільності, дотримуйтеся наступних інструкцій:
        
1. Незадовільна оцінка на мобільності сприймається як заборгованість і повинна бути ліквідована в наступному навчальному році.

2. Відповідно це тягне за собою ті ж самі наслідки, що й незадовільна оцінка в НаУКМА: переслуховування для бюджетників — переведення на контракт.

"""
    )
    return await generic_reply(update, text, [], FAILED_MOBILITY, back_button=True, home_button=True, back_home_row=True,
                               parse_mode=ParseMode.MARKDOWN)


mobility_handler = ConversationHandler(
    entry_points=[MessageHandler(filters.Regex('Мобільність'), mobility)],
    states={
        MOBILITY_CATEGORY: [
            MessageHandler(filters.Regex('Загальна інформація мобільність'), mobility_general),
            MessageHandler(filters.Regex('Програми мобільності'), mobility_programs),
            MessageHandler(filters.Regex('Самоініційована мобільність'), self_initiated_mobility),
            MessageHandler(filters.Regex('Порядок оформлення від’їзду'), departure_procedure),
            MessageHandler(filters.Regex('Порядок оформлення результатів'), results_procedure),
            MessageHandler(filters.Regex('Незарах на мобільності'), failed_mobility),
            MessageHandler(filters.Regex('Погодження'), approval),
            MessageHandler(filters.Regex(BACK), go_home),
        ],
        MOBILITY_GENERAL: [
            MessageHandler(filters.Regex(BACK), mobility),
            MessageHandler(filters.Regex(HOME), go_home),
        ],
        MOBILITY_PROGRAMS: [
            MessageHandler(filters.Regex(BACK), mobility),
            MessageHandler(filters.Regex(HOME), go_home),
        ],
        SELF_INITIATED_MOBILITY: [
            MessageHandler(filters.Regex(BACK), mobility),
            MessageHandler(filters.Regex(HOME), go_home),
        ],
        DEPARTURE_PROCEDURE: [
            MessageHandler(filters.Regex(BACK), mobility),
            MessageHandler(filters.Regex(HOME), go_home),
        ],
        RESULTS_PROCEDURE: [
            MessageHandler(filters.Regex(BACK), mobility),
            MessageHandler(filters.Regex(HOME), go_home),
        ],
        FAILED_MOBILITY: [
            MessageHandler(filters.Regex(BACK), mobility),
            MessageHandler(filters.Regex(HOME), go_home),
        ],
        APPROVAL: [
            MessageHandler(filters.Regex(BACK), mobility),
            MessageHandler(filters.Regex(HOME), go_home),
        ]
    },
    fallbacks=[CommandHandler('reset', fresh_start), CommandHandler('start', fresh_start),
               MessageHandler(filters.TEXT, unlucky)],
    name='mobility-handler',
    persistent=True,
)
