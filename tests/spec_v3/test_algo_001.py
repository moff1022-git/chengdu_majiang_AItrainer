import pytest
from engine.physical_tile import PHYSICAL_REGIONS, PhysicalOwnershipError, validate_physical_ownership

def regions(wall=range(108)):
    value={name: [] for name in PHYSICAL_REGIONS}; value["wall"]=list(wall); return value

def test_algo_001_golden_boundary_illegal_and_permutation():
    result = validate_physical_ownership(regions())
    assert result["conserved"] and result["face_counts"] == (4,) * 27
    permuted=regions(range(107,-1,-1)); assert result == validate_physical_ownership(permuted)
    duplicate=regions(); duplicate["hand:S0"]=[7]
    with pytest.raises(PhysicalOwnershipError) as exc: validate_physical_ownership(duplicate)
    assert exc.value.code == "OWNERSHIP_DUPLICATE"
    with pytest.raises(PhysicalOwnershipError) as exc: validate_physical_ownership(regions(range(107)))
    assert exc.value.code == "OWNERSHIP_MISSING"
    bad=regions(); bad["unknown"]=[]
    with pytest.raises(PhysicalOwnershipError) as exc: validate_physical_ownership(bad)
    assert exc.value.code == "REGION_UNKNOWN"
    missing=regions(); del missing["removed"]
    with pytest.raises(PhysicalOwnershipError) as exc: validate_physical_ownership(missing)
    assert exc.value.code == "REGION_MISSING"
