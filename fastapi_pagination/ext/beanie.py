__all__ = ["paginate"]

from typing import Optional, TypeVar, Union

from beanie import Document
from beanie.odm.queries.find import FindMany

from ..api import create_page
from ..bases import AbstractPage, AbstractParams
from ..types import AdditionalData
from ..utils import verify_params

TDocument = TypeVar("TDocument", bound=Document)


async def paginate(
    query: Union[TDocument, FindMany[TDocument]],
    params: Optional[AbstractParams] = None,
    *,
    additional_data: AdditionalData = None,
    fetch_links: bool = False,
) -> AbstractPage[TDocument]:
    params, raw_params = verify_params(params, "limit-offset")

    items = await query.find_many(limit=raw_params.limit, skip=raw_params.offset, fetch_links=fetch_links).to_list()
    total = await query.find({}, fetch_links=fetch_links).count()

    return create_page(items, total, params, **(additional_data or {}))
