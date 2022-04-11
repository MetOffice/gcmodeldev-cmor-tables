###############################################################################
# (c) Crown copyright 2022 Met Office. All rights reserved.
# The file LICENCE, distributed with this code, contains details of the terms
# under which the code may be used.
###############################################################################
"""
Entities defining the shape of the data
"""
from datetime import date
from typing import List, Optional, Union

from pydantic import BaseModel, Field


class CmorVariable(BaseModel):
    """
    Definition of a CMOR variable
    """
    id: str
    frequency: str
    standard_name: str
    units: str
    cell_methods: str
    cell_measures: str
    long_name: str
    comment: str
    dimensions: List[str]
    out_name: str
    type: str
    positive: str
    modeling_realm: Optional[List[str]] = None
    valid_min: Optional[float] = None
    valid_max: Optional[float] = None
    ok_min_mean_abs: Optional[float] = None
    ok_max_mean_abs: Optional[float] = None


class VariableTableHeader(BaseModel):
    """
    Definition of a CMOR Table Header Properties
    This could be merged directly into the table with a little restructuring
    """
    data_specs_version: str
    cmor_version: str
    table_id: str
    realm: str
    table_date: date
    missing_value: Optional[float]
    int_missing_value: Optional[int]
    product: str
    approx_interval: Optional[float]
    mip_era: str
    conventions: List[str]
    generic_levels: Optional[List[str]] = None


class VariableTable(BaseModel):
    """
    CMOR Table of Variables
    """
    header: VariableTableHeader
    variable_entry: Optional[List[CmorVariable]] = []


class Dimension(BaseModel):
    """
    Dimension Definition
    """
    id: str
    standard_name: str
    units: str
    axis: str
    long_name: str
    climatology: str
    formula: str
    must_have_bounds: bool
    out_name: str
    positive: str
    requested: Optional[List[Union[float, str]]]
    requested_bounds: Optional[List[Union[float, str]]]
    stored_direction: str
    tolerance: Optional[float]
    type: str
    valid_max: Optional[float]
    valid_min: Optional[float]
    value: Optional[Union[float, str]]
    z_bounds_factors: Optional[str]
    z_factors: Optional[str]
    bounds_values: Optional[str]
    generic_level_name: str


class Dimensions(BaseModel):
    """
    Collection of Dimension
    """
    axis_entry: List[Dimension]
