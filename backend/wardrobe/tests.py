from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient


User = get_user_model()


class DescriptionViewSerializerSmokeTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email="tester@example.com",
            password="strongpass123",
            first_name="Tester",
            last_name="User",
        )
        self.client.force_authenticate(user=self.user)

    def test_description_input_serializer_requires_one_of_image_or_image_url(self):
        response = self.client.post("/api/wardrobe/describe/", {}, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_description_input_serializer_rejects_mixed_image_inputs(self):
        image = SimpleUploadedFile("shirt.jpg", b"not-an-image", content_type="image/jpeg")
        payload = {
            "image": image,
            "image_url": "https://example.com/image.jpg",
        }
        response = self.client.post("/api/wardrobe/describe/", payload, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_clothing_description_schema_serializer_accepts_agent_shape(self):
        payload = {
            "type": {
                "name": "top",
                "subcategory": "t_shirt",
                "attributes": {
                    "sleeve_length": "short",
                    "sleeve_type": "regular",
                    "neckline": "crew",
                    "collar_type": "none",
                    "shoulder_style": "regular",
                    "hem_style": "straight",
                    "closure_type": "none",
                    "hood_type": "none",
                    "fit": "regular",
                    "length": "waist",
                },
            },
            "colors": [{"name": "black", "role": "primary", "percentage": 100}],
            "materials": [{"name": "cotton", "percentage": 100}],
            "patterns": [{"name": "solid", "scale": "none", "density": "none", "orientation": "none"}],
            "details": [],
            "styles": [{"name": "casual", "confidence": 0.8}],
            "pockets": [],
            "visual_attributes": {
                "dominant_color_hex": "#000000",
                "brightness": "dark",
                "saturation": "muted",
                "visual_complexity": "simple",
                "statement_level": "basic",
                "structure": "soft",
                "surface_finish": "matte",
                "transparency": "opaque",
                "symmetry": "symmetric",
            },
        }

        from wardrobe.serializers import ClothingDescriptionSchemaSerializer

        serializer = ClothingDescriptionSchemaSerializer(data=payload)
        self.assertTrue(serializer.is_valid(), serializer.errors)
