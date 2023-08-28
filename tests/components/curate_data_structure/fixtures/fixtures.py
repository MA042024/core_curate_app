""" Fixtures files for Data Structure
"""
from core_main_app.components.data.models import Data
from core_main_app.components.template.models import Template
from core_main_app.utils.integration_tests.fixture_interface import (
    FixtureInterface,
)
from django.core.files.uploadedfile import SimpleUploadedFile
from core_curate_app.components.curate_data_structure.models import (
    CurateDataStructure,
)


class DataStructureFixtures(FixtureInterface):
    """Data structure fixtures"""

    data_structure_1 = None
    data_structure_2 = None
    data_structure_3 = None
    data = None
    template = None
    data_collection = None

    def insert_data(self):
        """Insert a set of Data.

        Returns:

        """
        # Make a connexion with a mock database
        self.generate_template()
        self.generate_data_collection()

    def generate_data_collection(self):
        """Generate a Data collection.

        Returns:

        """

        # NOTE: no xml_content to avoid using unsupported GridFS mock
        self.data = Data(
            template=self.template,
            user_id="1",
            dict_content=None,
            title="title",
        )
        self.data.save()

        self.data_structure_1 = CurateDataStructure(
            user="1",
            template=self.template,
            name="data_structure_1",
            data=self.data,
        )
        self.data_structure_1.save()

        self.data_structure_2 = CurateDataStructure(
            user="1", template=self.template, name="data_structure_2"
        )
        self.data_structure_2.save()

        self.data_structure_3 = CurateDataStructure(
            user="2", template=self.template, name="data_structure_3"
        )
        self.data_structure_3.save()

        self.data_collection = [
            self.data_structure_1,
            self.data_structure_2,
            self.data_structure_3,
            self.data,
        ]

    def generate_template(self):
        """Generate an unique Template.

        Returns:

        """
        self.template = Template()
        xsd = (
            '<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema">'
            '<xs:element name="tag"></xs:element></xs:schema>'
        )
        self.template.file = SimpleUploadedFile(
            "user1_template.xsd", xsd.encode("utf-8")
        )
        self.template.user = "1"
        self.template.content = xsd
        self.template.hash = ""
        self.template.filename = "filename.xsd"
        self.template.save()


class DataStructureFixtures2(FixtureInterface):
    """Data structure fixtures"""

    data_structure_1 = None
    data_structure_2 = None
    data_structure_3 = None
    data = None
    data_without_draft = None
    data_multiple_drafts = None
    template = None
    data_collection = None

    def insert_data(self):
        """Insert a set of Data.

        Returns:

        """
        # Make a connexion with a mock database
        self.generate_template()
        self.generate_data_collection()

    def generate_data_collection(self):
        """Generate a Data collection.

        Returns:

        """

        # NOTE: no xml_content to avoid using unsupported GridFS mock
        self.data = Data(
            template=self.template,
            user_id="1",
            dict_content=None,
            title="title",
        )
        self.data.save()

        self.data_without_draft = Data(
            template=self.template,
            user_id="1",
            dict_content=None,
            title="title",
        )
        self.data_without_draft.save()

        self.data_multiple_drafts = Data(
            template=self.template,
            user_id="1",
            dict_content=None,
            title="title",
        )
        self.data_multiple_drafts.save()

        self.data_structure_1 = CurateDataStructure(
            user="1",
            template=self.template,
            name="data_structure_1",
            data=self.data,
        )
        self.data_structure_1.save()

        self.data_structure_2 = CurateDataStructure(
            user="1",
            template=self.template,
            name="data_structure_2",
            data=self.data_multiple_drafts,
        )
        self.data_structure_2.save()

        self.data_structure_3 = CurateDataStructure(
            user="2",
            template=self.template,
            name="data_structure_3",
            data=self.data_multiple_drafts,
        )
        self.data_structure_3.save()

        self.data_collection = [
            self.data_structure_1,
            self.data_structure_2,
            self.data_structure_3,
            self.data,
            self.data_without_draft,
            self.data_multiple_drafts,
        ]

    def generate_template(self):
        """Generate an unique Template.

        Returns:

        """
        self.template = Template()
        xsd = (
            '<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema">'
            '<xs:element name="tag"></xs:element></xs:schema>'
        )
        self.template.file = SimpleUploadedFile(
            "user1_template.xsd", xsd.encode("utf-8")
        )
        self.template.user = "1"
        self.template.content = xsd
        self.template.hash = ""
        self.template.filename = "filename.xsd"
        self.template.save()
