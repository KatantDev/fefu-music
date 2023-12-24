def format_duration(duration_ms: int) -> str:
    """
    Formats a duration in milliseconds to a string in the format hh:mm:ss, mm:ss or ss.

    Hours and minutes are omitted if they are 0.

    :param duration_ms: The duration in milliseconds.
    :return: The formatted duration.
    """
    seconds = duration_ms // 1000
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)

    duration_parts = []
    if hours > 0:
        duration_parts.append(f"{hours}".zfill(2))
    duration_parts.append(f"{minutes}".zfill(2))
    duration_parts.append(f"{seconds}".zfill(2))

    return ":".join(duration_parts)
