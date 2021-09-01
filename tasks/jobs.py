from twisted.internet import reactor
import time
import logging
import traceback
from django.conf import settings
from .models import CountBeansTask
from .models import SendEmailTask
from django_task.job import Job

from scrapy.crawler import CrawlerProcess, CrawlerRunner 
from scrapy.settings import Settings

from scraper.scraper import settings as lp_scraper_settings
from scraper.scraper.spiders.product_spider import ProductSpider

from apps.main.Crawlers.naverCrawler_downy import naverCrawler
from crawling.coupang_crawler import coupangCrawler

class ScraperJob(Job):

    @staticmethod
    def execute(job, task):
        num_beans = task.num_beans

        print("=========== 1================")
        crawler_settings = Settings()
        crawler_settings.setmodule(lp_scraper_settings)

        print("=========== 2================")
        runner = CrawlerRunner(settings=crawler_settings)

        print("=========== 3================")
        d = runner.crawl(ProductSpider)
        d.addBoth(lambda _: reactor.stop())
        reactor.run(0)

        # process = CrawlerProcess(settings=crawler_settings)
        # process.crawl(ProductSpider)
        # process.start()

        for i in range(0, num_beans):
            time.sleep(0.01)
            task.set_progress((i + 1) * 100 / num_beans, step=10)

    @staticmethod
    def on_complete(job, task):
        print('task "%s" completed with: %s' % (str(task.id), task.status))
        # 태스크 에러일 경우 처리 로직
        # if task.status != 'SUCCESS' or task.error_counter > 0:
        #    task.alarm = BaseTask.ALARM_STATUS_ALARMED
        #    task.save(update_fields=['alarm', ])

class navercrawlerJob(Job):

    @staticmethod
    def execute(job, task):
        

        print("=========== 1================")
        print("=========== 2================")
        print("=========== 3================")

        # print(__name__)
        nc = naverCrawler()
        nc.fcrawgo()




        # process = CrawlerProcess(settings=crawler_settings)
        # process.crawl(ProductSpider)
        # process.start()

    @staticmethod
    def on_complete(job, task):
        print('task "%s" completed with: %s' % (str(task.id), task.status))
        # 태스크 에러일 경우 처리 로직
        # if task.status != 'SUCCESS' or task.error_counter > 0:
        #    task.alarm = BaseTask.ALARM_STATUS_ALARMED
        #    task.save(update_fields=['alarm', ])

class coupangcrawlerJob(Job):
    
    @staticmethod
    def execute(job, task):
        

        print("======================= 1======================")
        print("======================= 2======================")
        print("======================= 3======================")
        print("===========coupang crawler start================")

        cc = coupangCrawler()
        cc.search_listup()
        cc.item_search()
        cc.item_review()




        # process = CrawlerProcess(settings=crawler_settings)
        # process.crawl(ProductSpider)
        # process.start()

    @staticmethod
    def on_complete(job, task):
        print('task "%s" completed with: %s' % (str(task.id), task.status))
        # 태스크 에러일 경우 처리 로직
        # if task.status != 'SUCCESS' or task.error_counter > 0:
        #    task.alarm = BaseTask.ALARM_STATUS_ALARMED
        #    task.save(update_fields=['alarm', ])












######################################################################################################################
class CountBeansJob(Job):

    @staticmethod
    def execute(job, task):
        num_beans = task.num_beans
        for i in range(0, num_beans):
            time.sleep(0.01)
            task.set_progress((i + 1) * 100 / num_beans, step=10)

    @staticmethod
    def on_complete(job, task):
        print('task "%s" completed with: %s' % (str(task.id), task.status))
        # An more realistic example from a real project ...
        # if task.status != 'SUCCESS' or task.error_counter > 0:
        #    task.alarm = BaseTask.ALARM_STATUS_ALARMED
        #    task.save(update_fields=['alarm', ])


class SendEmailJob(Job):

    @staticmethod
    def execute(job, task):
        recipient_list = task.recipients.split()
        sender = task.sender.strip()
        subject = task.subject.strip()
        message = task.message

        from django.core.mail import send_mail
        send_mail(subject, message, sender, recipient_list)
