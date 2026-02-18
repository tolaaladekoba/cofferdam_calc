def hydrostatic_pressure_at_depth(gamma_w: float, depth: float) -> float:
    """
    Hydrostatic pressure at a depth below the water surface.

    Formula:
        p = gamma_w * depth
    """
    return gamma_w * depth

