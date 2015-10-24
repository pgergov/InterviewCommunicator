from django.core.management.base import BaseCommand
from course_interviews.helpers.generate_students import GenerateStudents


class Command(BaseCommand):
    help = 'Make a request to f6s and add applicants with finalized forms'

    def handle(self, **options):
        f6s_address = "https://api.f6s.com/"
        f6s_application_name = "hackbulgaria-courses-fall2015"
        f6s_api_key = "g3WHBM4UYv"
        f6s_page_count = 100
        f6s_page = 1

        students_generator = GenerateStudents(
            f6s_address, f6s_application_name, f6s_api_key, f6s_page_count, f6s_page)

        students_generator.generate_students()
        generated_students = students_generator.get_generated_students()
        finalized_students = students_generator.get_students_with_finalized_applications()
        students_in_base = students_generator.get_students_in_base()

        print(str(generated_students) + ' students were generated')
        print('There are ' + str(
            finalized_students) + ' students with finalized applications and ' + str(
            students_in_base) + ' in the base')
