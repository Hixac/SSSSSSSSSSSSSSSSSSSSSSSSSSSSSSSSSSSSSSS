import pytest
from faker import Faker


fake = Faker()


@pytest.fixture
def sample_user_data() -> dict[str, str]:
    return {
        "name": fake.user_name(),
        "surname": fake.user_name(),
        "email": fake.email(),
        "password": fake.password(),
    }
