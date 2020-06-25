import sys
import os
from converter import Converter
def avi_to_mp4_with_converter(args):
  video_full_path = args[0]
  videos_save_path = args[1]
  test_video_hash = args[2]

  conv = Converter()
  info = conv.probe(video_full_path)
  # print(info.streams[0])
  print(dir(info.video))
  convert = conv.convert( video_full_path, 
                              '/var/www/html/process_trace_data/'+test_video_hash+'.mp4', {'format': 'mp4',
                              'audio': {
                                  'codec': 'aac',
                                  'samplerate': info.video.bitrate,
                                  'channels': 2
                              },
                              'video': {
                                  'codec': 'h264',
                                  'width': 320,
                                  'height': 240,
                                  'fps': info.video.video_fps   
                              }})
  for timecode in convert:
    print(f'\rConverting ({timecode:.2f}) ...')
  os.rename('/var/www/html/process_trace_data/'+test_video_hash+'.mp4',videos_save_path+test_video_hash+'.mp4')

if __name__ == "__main__":
    avi_to_mp4_with_converter(sys.argv[1:])