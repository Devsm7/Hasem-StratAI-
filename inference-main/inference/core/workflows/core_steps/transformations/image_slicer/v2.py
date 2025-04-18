from dataclasses import replace
from typing import List, Literal, Optional, Tuple, Type, Union
from uuid import uuid4

import numpy as np
from pydantic import AliasChoices, ConfigDict, Field, PositiveInt
from supervision import crop_image
from typing_extensions import Annotated

from inference.core.workflows.execution_engine.entities.base import (
    OutputDefinition,
    WorkflowImageData,
)
from inference.core.workflows.execution_engine.entities.types import (
    FLOAT_ZERO_TO_ONE_KIND,
    IMAGE_KIND,
    INTEGER_KIND,
    Selector,
)
from inference.core.workflows.prototypes.block import (
    BlockResult,
    WorkflowBlock,
    WorkflowBlockManifest,
)

LONG_DESCRIPTION = """
This block enables [Slicing Adaptive Inference (SAHI)](https://ieeexplore.ieee.org/document/9897990) technique in 
Workflows providing implementation for first step of procedure - making slices out of input image.

To use the block effectively, it must be paired with detection model (object-detection or 
instance segmentation) running against output images from this block. At the end - 
Detections Stitch block must be applied on top of predictions to merge them as if 
the prediction was made against input image, not its slices.

We recommend adjusting the size of slices to match the model's input size and the scale of objects in the dataset 
the model was trained on. Models generally perform best on data that is similar to what they encountered during 
training. The default size of slices is 640, but this might not be optimal if the model's input size is 320, as each 
slice would be downsized by a factor of two during inference. Similarly, if the model's input size is 1280, each slice 
will be artificially up-scaled. The best setup should be determined experimentally based on the specific data and model 
you are using.

To learn more about SAHI please visit [Roboflow blog](https://blog.roboflow.com/how-to-use-sahi-to-detect-small-objects/)
which describes the technique in details, yet not in context of Roboflow workflows.

#### Changes compared to **v1**

* All crops generated by slicer will be of equal size

* No duplicated crops will be created 
"""


class BlockManifest(WorkflowBlockManifest):
    model_config = ConfigDict(
        json_schema_extra={
            "name": "Image Slicer",
            "version": "v2",
            "short_description": "Tile the input image into a list of smaller images to perform small object detection.",
            "long_description": LONG_DESCRIPTION,
            "license": "Apache-2.0",
            "block_type": "transformation",
            "ui_manifest": {
                "section": "advanced",
                "icon": "fal fa-scissors",
                "blockPriority": 9,
                "opencv": True,
            },
        }
    )
    type: Literal["roboflow_core/image_slicer@v2"]
    image: Selector(kind=[IMAGE_KIND]) = Field(
        title="Image to slice",
        description="The input image for this step.",
        examples=["$inputs.image", "$steps.cropping.crops"],
        validation_alias=AliasChoices("image", "images"),
    )
    slice_width: Union[PositiveInt, Selector(kind=[INTEGER_KIND])] = Field(
        default=640,
        description="Width of each slice, in pixels",
        examples=[320, "$inputs.slice_width"],
    )
    slice_height: Union[PositiveInt, Selector(kind=[INTEGER_KIND])] = Field(
        default=640,
        description="Height of each slice, in pixels",
        examples=[320, "$inputs.slice_height"],
    )
    overlap_ratio_width: Union[
        Annotated[float, Field(ge=0.0, lt=1.0)],
        Selector(kind=[FLOAT_ZERO_TO_ONE_KIND]),
    ] = Field(
        default=0.2,
        description="Overlap ratio between consecutive slices in the width dimension",
        examples=[0.2, "$inputs.overlap_ratio_width"],
    )
    overlap_ratio_height: Union[
        Annotated[float, Field(ge=0.0, lt=1.0)],
        Selector(kind=[FLOAT_ZERO_TO_ONE_KIND]),
    ] = Field(
        default=0.2,
        description="Overlap ratio between consecutive slices in the height dimension",
        examples=[0.2, "$inputs.overlap_ratio_height"],
    )

    @classmethod
    def get_output_dimensionality_offset(cls) -> int:
        return 1

    @classmethod
    def describe_outputs(cls) -> List[OutputDefinition]:
        return [
            OutputDefinition(name="slices", kind=[IMAGE_KIND]),
        ]

    @classmethod
    def get_execution_engine_compatibility(cls) -> Optional[str]:
        return ">=1.3.0,<2.0.0"


class ImageSlicerBlockV2(WorkflowBlock):

    @classmethod
    def get_manifest(cls) -> Type[WorkflowBlockManifest]:
        return BlockManifest

    def run(
        self,
        image: WorkflowImageData,
        slice_width: int,
        slice_height: int,
        overlap_ratio_width: float,
        overlap_ratio_height: float,
    ) -> BlockResult:
        image_numpy = image.numpy_image
        resolution_wh = (image_numpy.shape[1], image_numpy.shape[0])
        offsets = generate_offsets(
            resolution_wh=resolution_wh,
            slice_wh=(slice_width, slice_height),
            overlap_ratio_wh=(overlap_ratio_width, overlap_ratio_height),
        )
        slices = []
        for offset in offsets:
            x_min, y_min, _, _ = offset
            crop_numpy = crop_image(image=image_numpy, xyxy=offset)
            if crop_numpy.size:
                cropped_image = WorkflowImageData.create_crop(
                    origin_image_data=image,
                    crop_identifier=f"image_slicer.{uuid4()}",
                    cropped_image=crop_numpy,
                    offset_x=x_min,
                    offset_y=y_min,
                )
                slices.append({"slices": cropped_image})
            else:
                slices.append({"slices": None})
        return slices


def generate_offsets(
    resolution_wh: Tuple[int, int],
    slice_wh: Tuple[int, int],
    overlap_ratio_wh: Tuple[float, float],
) -> np.ndarray:
    """
    This is modification of the function from block v1, which
    makes sure that the "border" crops are pushed towards the center of
    the image, making sure:
        * all crops will be the same size
        * deduplication of crops coordinates is done
    """
    slice_width, slice_height = slice_wh
    image_width, image_height = resolution_wh
    slice_width = min(slice_width, image_width)
    slice_height = min(slice_height, image_height)
    overlap_width = int(overlap_ratio_wh[0] * slice_width)
    overlap_height = int(overlap_ratio_wh[1] * slice_height)
    width_stride = slice_width - overlap_width
    height_stride = slice_height - overlap_height
    ws = np.arange(0, image_width, width_stride)
    ws_left_over = np.clip(ws + slice_width - image_width, 0, slice_width)
    hs = np.arange(0, image_height, height_stride)
    hs_left_over = np.clip(hs + slice_height - image_height, 0, slice_height)
    anchors_ws = ws - ws_left_over
    anchors_hs = hs - hs_left_over
    xmin, ymin = np.meshgrid(anchors_ws, anchors_hs)
    xmax = np.clip(xmin + slice_width, 0, image_width)
    ymax = np.clip(ymin + slice_height, 0, image_height)
    results = np.stack([xmin, ymin, xmax, ymax], axis=-1).reshape(-1, 4)
    deduplicated_results = []
    already_seen = set()
    for xyxy in results:
        xyxy_tuple = tuple(xyxy)
        if xyxy_tuple in already_seen:
            continue
        deduplicated_results.append(xyxy)
        already_seen.add(xyxy_tuple)
    return np.array(deduplicated_results)
