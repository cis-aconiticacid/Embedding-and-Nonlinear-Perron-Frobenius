

def hilbert_distance(x, y, eps=1e-8):
    """
    x, y: (m,) 正向量（>0）
    d_H(x, y) = log( max_i x_i / y_i ) - log( min_i x_i / y_i )

    返回: float
    """
    # 避免 0
    x_safe = x.clamp_min(eps)
    y_safe = y.clamp_min(eps)
    ratio = x_safe / y_safe
    max_r = ratio.max()
    min_r = ratio.min()
    return (max_r.log() - min_r.log()).item()