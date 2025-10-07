# Health schemas
from .health import (
    ComponentHealth,
    Health,
    DBHealth,
    S3Health,
)

# Dataset schemas
from .dataset import (
    DatasetBase,
    DatasetCreate,
    DatasetUpdate,
    Dataset,
    DatasetWithImages,
    DatasetWithLabels,
    DatasetDetail,
)

# Image schemas
from .image import (
    ImageBase,
    ImageCreate,
    ImageUpdate,
    Image,
    ImageWithDataset,
    ImageWithDownloadUrl,
    ImageStatus,
    ImageUploadRequest,
    ImageUploadResponse,
    ImageUploadBatchRequest,
    ImageUploadBatchResponse,
    ImageConfirmUploadRequest,
    ImageListResponse,
    ImageWithUrlListResponse,
)

# Label schemas
from .label import (
    LabelBase,
    LabelCreate,
    Label,
    LabelListResponse,
    LabelWithDatasets,
    LabelWithAnnotations,
)

# Annotation schemas
from .annotation import (
    AnnotationBase,
    AnnotationCreate,
    AnnotationUpdate,
    Annotation,
    AnnotationWithImage,
    AnnotationWithLabel,
    AnnotationWithImageAndLabel,
)

# Update forward references for all schemas
DatasetWithImages.model_rebuild()
DatasetWithLabels.model_rebuild()
ImageWithDataset.model_rebuild()
LabelListResponse.model_rebuild()
LabelWithDatasets.model_rebuild()
LabelWithAnnotations.model_rebuild()
AnnotationWithImage.model_rebuild()
AnnotationWithLabel.model_rebuild()
AnnotationWithImageAndLabel.model_rebuild()

__all__ = [
    # Health
    "ComponentHealth",
    "Health",
    "DBHealth",
    "S3Health",
    # Dataset
    "DatasetBase",
    "DatasetCreate",
    "DatasetUpdate",
    "Dataset",
    "DatasetWithImages",
    "DatasetWithLabels",
    "DatasetDetail",
    # Image
    "ImageBase",
    "ImageCreate",
    "ImageUpdate",
    "Image",
    "ImageWithDataset",
    "ImageWithDownloadUrl",
    "ImageStatus",
    "ImageUploadRequest",
    "ImageUploadResponse",
    "ImageUploadBatchRequest",
    "ImageUploadBatchResponse",
    "ImageConfirmUploadRequest",
    "ImageListResponse",
    "ImageWithUrlListResponse",
    # Label
    "LabelBase",
    "LabelCreate",
    "Label",
    "LabelListResponse",
    "LabelWithDatasets",
    "LabelWithAnnotations",
    # Annotation
    "AnnotationBase",
    "AnnotationCreate",
    "AnnotationUpdate",
    "Annotation",
    "AnnotationWithImage",
    "AnnotationWithLabel",
    "AnnotationWithImageAndLabel",
]
