# Health schemas
from .health import (
    ComponentHealth,
    Health,
    DBHealth,
    S3Health,
)

# Dataset schemas
from .dataset import (
    DatasetStatus,
    DatasetBase,
    DatasetCreate,
    DatasetUpdate,
    Dataset,
    DatasetWithImages,
)

# Image schemas
from .image import (
    ImageBase,
    ImageCreate,
    ImageUpdate,
    Image,
    ImageWithDataset,
)

# Label schemas
from .label import (
    LabelBase,
    LabelCreate,
    LabelUpdate,
    Label,
    LabelWithDataset,
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
ImageWithDataset.model_rebuild()
LabelWithDataset.model_rebuild()
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
    "DatasetStatus",
    "DatasetBase",
    "DatasetCreate",
    "DatasetUpdate",
    "Dataset",
    "DatasetWithImages",
    # Image
    "ImageBase",
    "ImageCreate",
    "ImageUpdate",
    "Image",
    "ImageWithDataset",
    # Label
    "LabelBase",
    "LabelCreate",
    "LabelUpdate",
    "Label",
    "LabelWithDataset",
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
