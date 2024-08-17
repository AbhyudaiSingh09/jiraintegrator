
def increment_version(version_number: str) -> int:
    try:
        incremented_version_number = int(version_number) + 1
    except ValueError:
        raise ValueError("Version number must be an integer")
    
    return incremented_version_number