import pytest

from model_bakery import baker
from rest_framework.test import APIClient

from students.models import Course, Student


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def course_factory():
    def factory(*args, **kwargs):
        return baker.make(Course, *args, **kwargs)

    return factory


@pytest.fixture
def students_factory():
    def factory(*args, **kwargs):
        return baker.make(Student, *args, **kwargs)

    return factory


@pytest.mark.django_db
def test_get_first_course(client, course_factory):
    course = course_factory(_quantity=1)
    response = client.get(f'/api/v1/courses/{course[0].id}/')
    response_data = response.json()

    assert response.status_code == 200
    assert response_data['id'] == course[0].id
    assert response_data['name'] == course[0].name


@pytest.mark.django_db
def test_get_all_courses(client, course_factory):
    courses = course_factory(_quantity=10)
    response = client.get('/api/v1/courses/')
    response_data = response.json()

    assert response.status_code == 200

    for idx, course in enumerate(response_data):
        assert course['id'] == courses[idx].id


@pytest.mark.django_db
def test_filter_course_by_id(client, course_factory):
    courses = course_factory(_quantity=10)
    response = client.get('/api/v1/courses/', data={'id': courses[0].id})
    response_data = response.json()

    assert response.status_code == 200
    assert response_data[0]['id'] == courses[0].id


@pytest.mark.django_db
def test_filter_course_name(client, course_factory):
    courses = course_factory(_quantity=10)
    response = client.get('/api/v1/courses/', data={'name': courses[0].name})
    response_data = response.json()

    assert response.status_code == 200
    assert response_data[0]['name'] == courses[0].name


@pytest.mark.django_db
def test_create_course(client):
    count = Course.objects.count()
    response = client.post('/api/v1/courses/', data={'name': 'demo_test'})

    assert response.status_code == 201
    assert Course.objects.count() == count + 1


@pytest.mark.django_db
def test_update_course(client, course_factory):
    courses = course_factory(_quantity=10)
    response = client.patch(f'/api/v1/courses/{courses[0].id}/', data={'name': 'test_update'})

    assert response.status_code == 200
    assert response.data['name'] == 'test_update'


@pytest.mark.django_db
def test_delete_course(client, course_factory):
    courses = course_factory(_quantity=10)
    count = Course.objects.count()
    response = client.delete(f'/api/v1/courses/{courses[0].id}/')

    assert response.status_code == 204
    assert Course.objects.count() == count - 1


# @pytest.mark.django_db
# def test_max_students_at_course(client, students_factory):
#     students = students_factory(_quantity=21)
#
#     course = Course.objects.create(name='test_course_name')
#     course.save()
#
#     for student in students:
#         course.students.add(student)
#         course.save()


@pytest.mark.parametrize('students_count,status_code', [(19, 201), (20, 201), (21, 400), ])
@pytest.mark.django_db
def test_max_students_at_course(client, students_factory, students_count, status_code):
    students = students_factory(_quantity=students_count)
    students_ids = [student.id for student in students]
    response = client.post('/api/v1/courses/', data={'name': 'Test', 'students': students_ids})

    assert response.status_code == status_code
