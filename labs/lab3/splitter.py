def create_segment(start_time):
    return {
        'segment_start_time': start_time,
        'segment_end_time': start_time,
        'data': []
    }


def split_data(data, interval=300):
    segments = []

    if not data:
        return []
    (start_time, _) = data[0]
    current_segment = create_segment(start_time)
    for time, value in data:
        if time - current_segment['segment_start_time'] > interval:
            segments.append(current_segment)
            current_segment = create_segment(time)

        current_segment['segment_end_time'] = time
        current_segment['data'].append((time, value))
    if current_segment['data']:
        segments.append(current_segment)
    return segments
