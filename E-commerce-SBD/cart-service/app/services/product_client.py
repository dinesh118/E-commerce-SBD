import os

import httpx
from dotenv import load_dotenv
from fastapi import HTTPException, status
from pydantic import BaseModel, ConfigDict, Field, ValidationError

load_dotenv()

PRODUCT_SERVICE_URL = os.getenv("PRODUCT_SERVICE_URL")
if not PRODUCT_SERVICE_URL:
    raise ValueError("PRODUCT_SERVICE_URL environment variable is required for cart service")
parsed_product_service_url = httpx.URL(PRODUCT_SERVICE_URL)
if parsed_product_service_url.scheme not in {"http", "https"} or not parsed_product_service_url.host:
    raise ValueError("PRODUCT_SERVICE_URL must be an absolute HTTP or HTTPS URL")
PRODUCT_SERVICE_URL = str(parsed_product_service_url).rstrip("/")

REQUEST_TIMEOUT = httpx.Timeout(5.0, connect=2.0)


class ProductDetails(BaseModel):
    model_config = ConfigDict(extra="ignore")

    id: int = Field(gt=0)
    name: str
    rate: float = Field(gt=0)
    stock: int = Field(ge=0)


def get_product_details(product_id: int, access_token: str) -> ProductDetails:
    try:
        response = httpx.get(
            f"{PRODUCT_SERVICE_URL}/products/{product_id}",
            headers={"Authorization": f"Bearer {access_token}"},
            timeout=REQUEST_TIMEOUT,
        )
    except httpx.TimeoutException as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Product service request timed out",
        ) from exc
    except httpx.RequestError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Product service is unavailable",
        ) from exc

    if response.status_code == status.HTTP_404_NOT_FOUND:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    if response.status_code != status.HTTP_200_OK:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Product service returned an unexpected response",
        )

    try:
        product = ProductDetails.model_validate(response.json())
    except (ValueError, ValidationError) as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Product service returned invalid product data",
        ) from exc
    if product.id != product_id:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Product service returned mismatched product data",
        )
    return product
