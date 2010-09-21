from django.test import TestCase

from nomore404.models import Pattern, ErrorRequest

class PatternTest(TestCase):

    def test_wildcard_match(self):
        """Test that matching against filters worked correctly"""

        wildcard = Pattern.objects.create(regex=".*")
        self.assertTrue(Pattern.objects.matches("boom"))
        wildcard.delete()

    def test_fail_match(self):

        wildcard = Pattern.objects.create(regex="blergh.*")
        wildcard1 = Pattern.objects.create(regex="blergh.*town")
        self.assertFalse(Pattern.objects.matches("hey"))
        wildcard.delete()
        wildcard1.delete()

    def test_complex_match(self):
        """Test that matching against filters worked correctly"""

        patterns = [Pattern.objects.create(regex=pattern) for pattern in \
                    ["a.*b", "b.*c", "d.*e", "e.*f"]]

        self.assertTrue(Pattern.objects.matches("aaaacccbbbb"))
        self.assertTrue(Pattern.objects.matches("eeeeffff"))
        self.assertFalse(Pattern.objects.matches("zzzzzyyyy"))

        for pattern in patterns:
            pattern.delete()


    def test_save_delete(self):
        """Test deleting ErrorRequests when a new pattern is saved"""

        ErrorRequest.objects.create(path="boom", request="None")
        ErrorRequest.objects.create(path="boom1", request="None")
        ErrorRequest.objects.create(path="boom2", request="None")

        self.assertEquals(ErrorRequest.objects.filter(path="boom").count(), 1)
        self.assertEquals(ErrorRequest.objects.filter(path="boom1").count(), 1)
        self.assertEquals(ErrorRequest.objects.filter(path="boom2").count(), 1)

        wildcard = Pattern.objects.create(regex="boom.*")

        self.assertEquals(ErrorRequest.objects.filter(path="boom").count(), 0)
        self.assertEquals(ErrorRequest.objects.filter(path="boom1").count(), 0)
        self.assertEquals(ErrorRequest.objects.filter(path="boom2").count(), 0)


class ErrorTest(TestCase):

    def test_save(self):

        error = ErrorRequest.objects.create(path="boom", request="None")
        self.assertEquals(ErrorRequest.objects.filter(path="boom").count(), 1)

        wildcard = Pattern.objects.create(regex="boom.*")
        self.assertEquals(ErrorRequest.objects.filter(path="boom").count(), 0)
        
        error = ErrorRequest.objects.create(path="boom", request="None")
        self.assertEquals(ErrorRequest.objects.filter(path="boom").count(), 0)

        wildcard.delete()
        error = ErrorRequest.objects.create(path="boom", request="None")
        self.assertEquals(ErrorRequest.objects.filter(path="boom").count(), 1)

        error.delete()
