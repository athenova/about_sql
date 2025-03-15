from simple_blogger import CommonBlogger
from simple_blogger.generators.OpenAIGenerator import OpenAITextGenerator
from datetime import datetime
from datetime import timedelta
from simple_blogger.senders.TelegramSender import TelegramSender
#from simple_blogger.senders.InstagramSender import InstagramSender

class Project(CommonBlogger):
    def _example_task_creator(self):
        return [
            {
                "domain": "domain",
                "technology": "technology",
                "soft": "soft",
                "problem": "problem"
            }
        ]

    def _get_category_folder(self, task):
        return f"{task['technology']}/{task['soft']}"
                    
    def _get_topic_folder(self, task):
        return f"{task['problem']}"

    def _system_prompt(self, task):
        return "Ты - архитектор решений"

    def _task_converter(self, idea):
        return { 
                    "soft": idea['soft'],
                    "problem": idea['problem'],
                    "technology": idea['technology'],
                    "description_prompt": f"Опиши проблему '{idea['problem']}' связанную с технологией '{idea['technology']}' и программным средством '{idea['soft']}' из области '{idea['domain']}', не описывай решение, используй не более {self.topic_word_limit} слов",
                    "description_image": f"Нарисуй рисунок, вдохновлённый проблемой '{idea['problem']}' связанную с технологией '{idea['technology']}' и программным средством '{idea['soft']}' из области '{idea['domain']}'",
                    "solution_prompt": f"Опиши решение проблемы '{idea['problem']}' связанной с технологией '{idea['technology']}' и программным средством '{idea['soft']}' из области '{idea['domain']}', используй не более {self.topic_word_limit} слов",
                    "solution_image": f"Нарисуй рисунок, вдохновлённый решением проблемы '{idea['problem']}' связанной с технологией '{idea['technology']}' и программным средством '{idea['soft']}' из области '{idea['domain']}'",
                }

    def __init__(self, **kwargs):
        super().__init__(
            first_post_date=datetime(2025, 3, 3),
            text_generator=OpenAITextGenerator(),
            topic_word_limit=300,
            shuffle_tasks=False,
            days_between_posts=timedelta(days=7),
            days_to_review=timedelta(days=2),
            reviewer=TelegramSender(channel_id=-1002396564369, send_text_with_image=False),
            senders=[TelegramSender(channel_id=f"@about_sql", send_text_with_image=False)],
            **kwargs
        )

    