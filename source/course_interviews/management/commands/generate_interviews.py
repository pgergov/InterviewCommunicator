from django.core.management.base import BaseCommand
from course_interviews.helpers import GenerateInterviews


class Command(BaseCommand):
    help = 'Make a request to f6s and add applicants with finalized forms'

    def handle(self, **options):
        interview_generator = GenerateInterviews()
        interview_generator.generate_interviews()

        students_without_interviews = interview_generator.get_students_without_interviews()
        generated_interviews = interview_generator.get_generated_interviews_count()

        print(str(generated_interviews) + ' interviews were generated')
        print(str(students_without_interviews) + ' students do not have interview date')