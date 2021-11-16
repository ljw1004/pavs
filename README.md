# .pst / .psf / PAVS video file format, from security cameras

I'd like to figure out the video format for backed up video from my security camera system. The system is controlled and monitored by a desktop machine running "VMax Client" software which records video from multiple cameras onto disk, (I think) can upload video to the cloud, lets you review historical video, and lets you backup video to USB:
![av-backup](https://user-images.githubusercontent.com/3316258/141853620-396def5d-fc59-4822-99af-33551f547abc.jpg)

The backup produces (1) a single `.pst` file, (2) a load of `.psf` files, each up to about 700mb and containing footage from one or more cameras for up to about 12 hours, (3) a windows executable that can play those files `Player.exe, avcodec-52.dll, avformat-52.dll, avutil-50.dll, libfaac.dll, ...`. Here's what it looks like when you play video:

https://user-images.githubusercontent.com/3316258/141854196-cbe3d804-ae89-4d50-b58f-93b04a0a8169.mp4

[This link](https://superuser.com/a/790140) claims you can download the software "VMax ACS Playback for Windows/Mac". From that link, the Windows software installs two programs into "C:\Program Files (x86)" - (1) the VMax Client sofware for receiving live data from security cameras, and (2) the player. The Mac software seems to only incldue the VMax Client, not the player. Lots of people have asked how to convert .psf files into other formats [[link1](https://community.spiceworks.com/topic/753755-how-to-convert-psf-to-avi-or-mpeg), [link2](https://www.reddit.com/r/techsupport/comments/bi53e4/i_have_some_video_files_in_psf_that_i_need_to/), [link3](https://www.reddit.com/r/techsupport/comments/2k0ib0/how_to_play_psf_files/), [link4](https://www.reddit.com/r/cctv/comments/9wq2qc/converting_psf_to_any_sort_of_common_video_file/), [link5](https://www.reddit.com/r/techsupport/comments/2nfyk1/what_program_plays_a_psf_video_on_a_mac/), [link6](https://www.reddit.com/r/ITdept/comments/9so463/convert_multi_camera_to_psf/)] but no one has succeeded so far - the files don't open in VLC nor Handbrake nor K-Lite Codec Pack.

***Can I figure out the video format of .psf files and convert them to mp4 myself?***

## Inspection of an example backup

I backed up video from camera 9 of my home's security system. It produced a 734mb file spanning 2021-09-01 12:00:01 to 13:50:00 (49800 seconds). Interacting with the player, it seemed to show 2fps (99600 frames), although when I clicked the "export" button it was only willing to export one still image per second. Those still images claimed 704x240 resolution, and were in color.

Eyeballing the file I see it has 99498 "PAVS" blocks one after the other. That's so close to the expected number of frames that I'm sure there's one PAVS block every half second and I just didn't count seconds quite right. Each block has almost identical 0x248 bytes of header. Here are two examples.

```
frame 0 (0x1A00 bytes long)
00000000  50 41 56 53 02 09 00 00  03 02 03 02 2d 00 00 00  |PAVS........-...|
00000010  2a 1f eb c0 00 00 00 00  00 00 00 00 00 42 54 ea  |*............BT.|
00000020  3d 00 00 00 00 42 54 ea  3d 00 00 00 80 e0 c2 05  |=....BT.=.......|
00000030  c0 09 59 7e c2 35 cd 21  00 0c 00 00 00 1a 00 00  |..Y~.5.!........|
00000040  01 08 01 00 00 00 00 00  db 15 00 00 40 00 00 00  |............@...|
00000050  c0 02 f0 00 01 02 02 00  00 f7 01 00 41 4c 4c 45  |............ALLE|
00000060  59 00 53 69 64 65 00 65  00 00 00 00 00 00 00 00  |Y.Side.e........|
00000070  02 00 00 00 00 00 00 00  80 08 00 00 00 00 00 00  |................|
00000080  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
000001f0  00 00 00 00 00 00 00 00  00 00 00 00 71 a3 04 82  |............q...|
00000200  db 15 20 08 0f 2c 0e 11  c0 97 3b 07 00 22 82 06  |.. ..,....;.."..|
00000210  40 00 f0 00 f1 24 2f 61  30 ef 06 00 00 00 00 00  |@....$/a0.......|
00000220  48 f9 82 bf 08 00 00 00  db 15 00 00 0f 00 00 00  |H...............|
00000230  01 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
00000240  00 00 00 01 65 88 80 20  00 4c 60 23 ff c2 50 1c  |....e.. .L`#..P.|
00000250  00 08 81 c2 52 96 e7 d4  3f 96 e7 8f c2 e0 50 7d  |....R...?.....P}|

frame 42052 (0x2000 bytes long)
00000000  50 41 56 53 02 09 00 00  03 02 03 02 2d 00 00 00  |PAVS........-...|
00000010  42 1f eb c0 00 00 00 00  00 00 00 00 00 e8 55 ea  |B.............U.|
00000020  3d 00 00 00 00 e8 55 ea  3d 00 00 00 80 e0 b6 07  |=.....U.=.......|
00000030  c0 09 59 7e c7 35 cd 21  00 0c 00 00 00 0a 00 00  |..Y~.5.!........|
00000040  01 08 01 00 00 00 00 00  aa 06 00 00 40 00 00 00  |............@...|
00000050  c0 02 f0 00 01 02 02 00  01 f7 01 00 41 4c 4c 45  |............ALLE|
00000060  59 00 53 69 64 65 00 65  00 00 00 00 00 00 00 00  |Y.Side.e........|
00000070  02 00 00 00 00 00 00 00  40 07 00 00 00 00 00 00  |........@.......|
00000080  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
000001f0  00 00 00 00 00 00 00 00  00 00 00 00 ac af 70 80  |..............p.|
00000200  aa 06 60 08 0f 2c 0f 11  80 44 3d 07 40 81 85 06  |..`..,...D=.@...|
00000210  40 00 f0 00 f1 24 2f 61  4d 92 0e 00 00 00 00 00  |@....$/aM.......|
00000220  6e 23 0d df 08 00 00 00  aa 06 00 00 00 00 00 00  |n#..............|
00000230  01 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
00000240  00 00 00 01 41 9a 01 00  b0 98 8f 13 ff ff ff ff  |....A...........|
00000250  ff ff fe 6e 3a d7 f1 7c  a4 78 3b 92 f8 be 7a 6f  |...n:..|.x;...zo|
```

What we see:
* Offset 0x0000 of each PAVS block is the magic word "PAVS"
* Offset 0x003C is the size of this entire PAVS block from start to end
* Offset 0x005C is a pair of null-terminated ASCII strings with the user-specified name of this camera
* Offset 0x0248 until the end fo the block appears to be high-entropy encoded data

I wrote `get_frames.py` in this repository to scan a .psf file and emit offsets of each PAVS block, e.g.
```
tail -c +1 vid.psf | head -c 6656 > frame00000_0h00m00.0s.raw && hexdump -C frame00000_0h00m00.0s.raw > frame00000_0h00m00.0s.hex
tail -c +6657 vid.psf | head -c 2560 > frame00001_0h00m00.5s.raw && hexdump -C frame00001_0h00m00.5s.raw > frame00001_0h00m00.5s.hex
tail -c +9217 vid.psf | head -c 6656 > frame00002_0h00m01.0s.raw && hexdump -C frame00002_0h00m01.0s.raw > frame00002_0h00m01.0s.hex
tail -c +15873 vid.psf | head -c 2560 > frame00003_0h00m01.5s.raw && hexdump -C frame00003_0h00m01.5s.raw > frame00003_0h00m01.5s.hex
```

Here are some sequentail PAVS file-sizes in my video:
```
6656, 2560, 6656, 2560, ..., 8192, 3072, 8192, 3072, ..., 13312, 3584, 12800, 3584, 12800, 3584, 13312, 3584, ...
```
The entire file had this repeating pattern of big, small, big, small. The larger sizes were at times of the day where there
was more detail in the picture, or more happening.
My hunch is that each even frame is an entire picture, and each odd frame is a delta on top of it.

Wikipedia notes that PFS stands for [Progressive Segmented Frame](https://en.wikipedia.org/wiki/Progressive_segmented_frame):
"With PsF, a progressive frame is divided into two segments, with the odd lines in one segment and the even lines in the other segment. Technically, the segments are equivalent to interlaced fields, but unlike native interlaced video, there is no motion between the two fields that make up the video frame: both fields represent the same instant in time. This technique allows for a progressive picture to be processed through the same electronic circuitry that is used to store, process and route interlaced video." But I don't think this is related.

## Producing my own video data

I extracted out several frames using the `get_frames.py` script in this repository. For each frame, I opened it in Player.exe and tried to export frames
to disk as images. It was hard export every single frame, and hard to know which of the exported images correspond to which frame.
* frame0 [raw](https://github.com/ljw1004/pavs/blob/main/frames/frame00000.raw) [hex](https://github.com/ljw1004/pavs/blob/main/frames/frame00000.hex), frame1 [raw](https://github.com/ljw1004/pavs/blob/main/frames/frame00001.raw) [hex](https://github.com/ljw1004/pavs/blob/main/frames/frame00001.hex)
* frame2 [raw](https://github.com/ljw1004/pavs/blob/main/frames/frame00002.raw) [hex](https://github.com/ljw1004/pavs/blob/main/frames/frame00002.hex), frame3 [raw](https://github.com/ljw1004/pavs/blob/main/frames/frame00003.raw) [hex](https://github.com/ljw1004/pavs/blob/main/frames/frame00003.hex)
* frame4 [raw](https://github.com/ljw1004/pavs/blob/main/frames/frame00004.raw) [hex](https://github.com/ljw1004/pavs/blob/main/frames/frame00004.hex), frame5 [raw](https://github.com/ljw1004/pavs/blob/main/frames/frame00005.raw) [hex](https://github.com/ljw1004/pavs/blob/main/frames/frame00005.hex)
* images: [00:00:01.jpg](https://github.com/ljw1004/pavs/blob/main/frames/frame_at_000001.jpg), [00:00:02a.jpg](https://github.com/ljw1004/pavs/blob/main/frames/frame_at_000002a.jpg), [00:00:02b.jpg](https://github.com/ljw1004/pavs/blob/main/frames/frame_at_000002b.jpg), [00:00:02c.jpg](https://github.com/ljw1004/pavs/blob/main/frames/frame_at_000002c.jpg), [00:00:03.jpg](https://github.com/ljw1004/pavs/blob/main/frames/frame_at_000003.jpg)
* frame42052 [raw](https://github.com/ljw1004/pavs/blob/main/frames/frame42052.raw) [hex](https://github.com/ljw1004/pavs/blob/main/frames/frame42052.hex), frame42053 [raw](https://github.com/ljw1004/pavs/blob/main/frames/frame42053.raw) [hex](https://github.com/ljw1004/pavs/blob/main/frames/frame42053.hex)
* frame42054 [raw](https://github.com/ljw1004/pavs/blob/main/frames/frame42054.raw) [hex](https://github.com/ljw1004/pavs/blob/main/frames/frame42054.hex), frame42055 [raw](https://github.com/ljw1004/pavs/blob/main/frames/frame42055.raw) [hex](https://github.com/ljw1004/pavs/blob/main/frames/frame42055.hex)
* frame42056 [raw](https://github.com/ljw1004/pavs/blob/main/frames/frame42056.raw) [hex](https://github.com/ljw1004/pavs/blob/main/frames/frame42056.hex), frame42057 [raw](https://github.com/ljw1004/pavs/blob/main/frames/frame42055.raw) [hex](https://github.com/ljw1004/pavs/blob/main/frames/frame42057.hex)
* images: [05:50:48.jpg](https://github.com/ljw1004/pavs/blob/main/frames/frame_at_055048.jpg), [05:50:49.jpg](https://github.com/ljw1004/pavs/blob/main/frames/frame_at_055049.jpg), [05:50:50.jpg](https://github.com/ljw1004/pavs/blob/main/frames/frame_at_055050.jpg)
* frame71760 [raw](https://github.com/ljw1004/pavs/blob/main/frames/frame71760.raw) [hex](https://github.com/ljw1004/pavs/blob/main/frames/frame71760.hex), frame71761 [raw](https://github.com/ljw1004/pavs/blob/main/frames/frame71761.raw) [hex](https://github.com/ljw1004/pavs/blob/main/frames/frame71761.hex)
* frame71762 [raw](https://github.com/ljw1004/pavs/blob/main/frames/frame71762.raw) [hex](https://github.com/ljw1004/pavs/blob/main/frames/frame71762.hex), frame71763 [raw](https://github.com/ljw1004/pavs/blob/main/frames/frame71763.raw) [hex](https://github.com/ljw1004/pavs/blob/main/frames/frame71763.hex)
* frame71764 [raw](https://github.com/ljw1004/pavs/blob/main/frames/frame71764.raw) [hex](https://github.com/ljw1004/pavs/blob/main/frames/frame71764.hex), frame71765 [raw](https://github.com/ljw1004/pavs/blob/main/frames/frame71765.raw) [hex](https://github.com/ljw1004/pavs/blob/main/frames/frame71765.hex)
* images: [09:58:37.jpg](https://github.com/ljw1004/pavs/blob/main/frames/frame_at_095837.jpg), [09:58:38a.jpg](https://github.com/ljw1004/pavs/blob/main/frames/frame_at_095838a.jpg), [09:58:38b.jpg](https://github.com/ljw1004/pavs/blob/main/frames/frame_at_095838b.jpg), [09:58:39.jpg](https://github.com/ljw1004/pavs/blob/main/frames/frame_at_095839.jpg), [09:58:40.jpg](https://github.com/ljw1004/pavs/blob/main/frames/frame_at_095840.jpg), 

I used `cat` to cobble together some frames to make my own .psf video file.

**Video1** stiches together all big-small pairs above (18 frames in total).
* `cat` frames 0,1,2,3,4,5, 42052,42053,42054,42055,42056,42057, 71760,71761,71762,71763,71764,71765 > [video1.psf](https://github.com/ljw1004/pavs/blob/main/videos/video1.psf)
* Observation: [video1_player.mp4](https://github.com/ljw1004/pavs/blob/main/videos/video1_player.mp4). It played fine in the player. It showed three seconds from early in the day, 3 seconds from the middle of the day, 3 seconds from later in the day.

**Video2** stiches the three ascending time sequences in reverse order.
* `cat` frames 71760,71761,71762,71763,71764,71765, 42052,42053,42054,42055,42056,42057, 0,1,2,3,4,5 > [video2.psf](https://github.com/ljw1004/pavs/blob/main/videos/video2.psf)
* Observations: [video2_player.mp4](https://github.com/ljw1004/pavs/blob/main/videos/video2_player.mp4). It played fine, as expected, but the UI controls in Player.exe showed it jumping around in the timeline which made it hard to navigate.

**Video3** tries to use the wrong "small" frames.
* `cat` frames 0,1,0,3,0,5, 0,42053,0,42055,0,42057, 0,71761,0,71763,0,71765 > [video3.psf](https://github.com/ljw1004/pavs/blob/main/videos/video3.psf)
* Observations: [video3_player.mp4](https://github.com/ljw1004/pavs/blob/main/videos/video3_player.mp4). It didn't seem to work. I minor frames aren't purely a diff on the preceding major frame; they must also contain
some other kind of tie-in.

## What encoding?

I looked at the size distributions of even and odd frames.
```
 EVEN FRAMES          ODD FRAMES
count size          count size
---------------------------------
  503  6144             4  2048
12438  6656         17275  2560
   34  7168         15067  3072
 2325  7680          7205  3584
 6724  8192             1  3640
  207  8704          4353  4096
   76  9216          2613  4608
   97  9728          1459  5120
   36 10240           753  5632
   26 10752           411  6144
  492 11264           221  6656
 1954 11776           136  7168
 1774 12288            83  7680
 1535 12800            91  8192
 1747 13312            21  8704
 3061 13824            11  9216
 1835 14336             6  9728
 2423 14848             4 10240
 1722 15360             6 10752
 1280 15872             4 11264
 3461 16384             5 11776
 2661 16896             4 12288
 1866 17408             3 12800
  787 17920             1 13312
  282 18432             3 13824
  370 18944             4 14336
   22 19456             2 14848
    7 19968             2 15360
    4 20480             1 15872
```

It's clear that the frames are compressed somehow! But I have no idea what encoding.

I looked at the `dumpbin /exports` of the DLLs in the player to see if there were any hints about codec.
It's unclear, though, since I don't know if Player.exe uses each DLL to read the .psf file or
to export JPG still images or MP4 clips.
* [dumpbin /exports avcodec-52.dll](https://github.com/ljw1004/pavs/blob/main/dlls/avcodec-52.dll.dumpbin) - part of FFMPEG
* [dumpbin /exports avformat-52.dll](https://github.com/ljw1004/pavs/blob/main/dlls/avformat-52.dll.dumpbin) - part of FFMPEG
* [dumpbin /exports avutil-50.dll](https://github.com/ljw1004/pavs/blob/main/dlls/avutil-50.dll.dumpbin) - parg of FFMPEG
* [dumpbin /exports swscale-0.dll](https://github.com/ljw1004/pavs/blob/main/dlls/swscale-0.dll.dumpbin) - part of FFMPEG
* [dumpbin /exports libfaac.dll](https://github.com/ljw1004/pavs/blob/main/dlls/libfaac.dll.dumpbin) - part of FFMPEG
* [dumpbin /imports player.exe](https://github.com/ljw1004/pavs/blob/main/dlls/player.exe.dumpbin)...
   * from avcodec-52.dll: audio_resample, audio_resample_close, audio_resample_init, av_init_packet, avcodec_alloc_context, avcodec_alloc_frame, avcodec_close, avcdec_decode_audio3, avcodec_decode_video2, avcodec_encode_audio, avcodec_encode_video, avcodec_find_decoder, avcodec_find_encoder, avcodec_init, avcodec_deinterlace, avpicture_fill, avpicture_get_size
   * from avformat-52.dll: av_interleaved_write_frame, av_new_stream, av_register_all, av_write_header, av_write_trailer, avformat_alloc_output_context2, url_fclose, url_fopen
   * from avutil-50.dll: av_free, av_freep, av_log_set_callback, av_malloc, av_rescale_q
   * from swscale-0.dll: sws_freeContext, sws_getCachedContext, sws_scale
   * from libfaac.dll: faacEncClose, faacEncEncode, faacEncGetCurrentConfiguration, faacEncOpen, faacEncSetConfiguration

All the DLLs are part of FFMPEG. Therefore: either Player.exe uses an off-the-shelf codec from FFMPEG to read .psf files, or it uses its own. My guess is off-the-shelf.

Eyeballing the PSAV frames, I see that each one (both odd and even) has the exact same four bytes `00 00 00 01` at offset 0x240, which looks like a familiar [H.264 NAL](https://stackoverflow.com/questions/38094302/how-to-understand-header-of-h264). Here's an example:
```
EVEN FRAME
00000230  01 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
00000240  00 00 00 01 65 88 80 20  00 4c 60 23 ff c2 50 1c  |....e.. .L`#..P.|
00000250  00 08 81 c2 52 96 e7 d4  3f 96 e7 8f c2 e0 50 7d  |....R...?.....P}|

ODD FRAME
00000230  01 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
00000240  00 00 00 01 41 9a 01 00  b0 9f ff f0 61 e1 4f 02  |....A.......a.O.|
00000250  2f ff ff ff ff 9b d8 5e  2f b4 81 6c fe 2f 48 84  |/......^/..l./H.|
```
After `00 00 00 01` comes the NAL header byte [[walkthrough of NAL headers](https://yumichan.net/video-processing/video-compression/introduction-to-h264-nal-unit/)], in this case always `65` for even frames (nal_unit_type "Coded slice of an IDR picture") and `41` for odd frames (nal_unit_type "Coded slice of a non-IDR picture"). IDR means that it's a full image that can be understood on its own; non-IDR means it needs to reference an earlier frame. This agrees with our "big frame / small frame" observation.

## Decoding the h264

Here is some information on h264 file format:
* https://www.cardinalpeak.com/blog/worlds-smallest-h-264-encoder
* https://www.cardinalpeak.com/blog/the-h-264-sequence-parameter-set

A minimal h264 must consists of an SPS 0x67 NAL, a PPS 0x68 NAL, and an IDR 0x65 NAL.
There's no sign of the SPS or PPS in each PVAS, so I suppose that Player.exe must
synthesize them itself. I tried cobbling together an SPS and PPS myself:
```
$ printf '\x00\x00\x00\x01\x67\x42\x00\x0a\xf8\x16\x0f\x88' > sps
$ printf '\x00\x00\x00\x01\x68\xce\x38\x80' > pps
$ tail -c +577 frames/frame00000.raw > idr
$ cat sps pps idr > all.h264
$ ffmpeg -i all.h264 -c copy -bsf:v trace_headers -f null -
```
Here's how ffmpeg decoded my SPS, my PPS, and the IDR from the PAVS frame. I picked `pic_width_in_mbs_minus1 = 43` since macroblocks (mbs) are 16x16, and 44\*16=704, the pixel width of the image. I picked `pic_height_in_map_units_minus1 = 14` since 14\*16=240. I didn't have a clue what to put for the other parameters and just guessed.
It's reading of the IDR slice header it got from the PAVS frame looks correct; `slice_type=7` indicates an I slice type, which is right.
```
SPS (Sequence Parameter Set)
forbidden_zero_bi                                       0 = 0
nal_ref_idc                                            11 = 3
nal_unit_type                                       00111 = 7
profile_idc                                      01000010 = 66
constraint_set0_flag                                    0 = 0
constraint_set1_flag                                    0 = 0
constraint_set2_flag                                    0 = 0
constraint_set3_flag                                    0 = 0
constraint_set4_flag                                    0 = 0
constraint_set5_flag                                    0 = 0
reserved_zero_2bits                                    00 = 0
level_idc                                        00001010 = 10
seq_parameter_set_id                                    1 = 0
log2_max_frame_num_minus4                               1 = 0
pic_order_cnt_type                                      1 = 0
log2_max_pic_order_cnt_lsb_minus4                       1 = 0
max_num_ref_frames                                      1 = 0
gaps_in_frame_num_allowed_flag                          0 = 0
pic_width_in_mbs_minus1                       00000101100 = 43
pic_height_in_map_units_minus1                    0001111 = 14
frame_mbs_only_flag                                     1 = 1
direct_8x8_inference_flag                               0 = 0
frame_cropping_flag                                     0 = 0
vui_parameters_present_flag                             0 = 0
rbsp_stop_one_bit                                       1 = 1
rbsp_alignment_zero_bit                                 0 = 0
rbsp_alignment_zero_bit                                 0 = 0
rbsp_alignment_zero_bit                                 0 = 0


(PPS) Picture Parameter Set
forbidden_zero_bit                                      0 = 0
nal_ref_idc                                            11 = 3
nal_unit_type                                       01000 = 8
pic_parameter_set_id                                    1 = 0
seq_parameter_set_id                                    1 = 0
entropy_coding_mode_flag                                0 = 0
bottom_field_pic_order_in_frame_present_flag            0 = 0
num_slice_groups_minus1                                 1 = 0
num_ref_idx_l0_default_active_minus1                    1 = 0
num_ref_idx_l1_default_active_minus1                    1 = 0
weighted_pred_flag                                      0 = 0
weighted_bipred_idc                                    00 = 0
pic_init_qp_minus26                                     1 = 0
pic_init_qs_minus26                                     1 = 0
chroma_qp_index_offset                                  1 = 0
deblocking_filter_control_present_flag                  0 = 0
constrained_intra_pred_flag                             0 = 0
redundant_pic_cnt_present_flag                          0 = 0
rbsp_stop_one_bit                                       1 = 1
rbsp_alignment_zero_bit                                 0 = 0
rbsp_alignment_zero_bit                                 0 = 0
rbsp_alignment_zero_bit                                 0 = 0
rbsp_alignment_zero_bit                                 0 = 0
rbsp_alignment_zero_bit                                 0 = 0
rbsp_alignment_zero_bit                                 0 = 0
rbsp_alignment_zero_bit                                 0 = 0


IDR (Slice Header)
forbidden_zero_bit                                      0 = 0
nal_ref_idc                                            11 = 3
nal_unit_type                                       00101 = 5
first_mb_in_slice                                       1 = 0
slice_type                                        0001000 = 7
pic_parameter_set_id                                    1 = 0
frame_num                                            0000 = 0
idr_pic_id                                    00000100000 = 31
pic_order_cnt_lsb                                    0000 = 0
no_output_of_prior_pics_flag                            0 = 0
long_term_reference_flag                                0 = 0
slice_qp_delta                                    0001001 = -4
```

Unfortunately it failed to decode. It didn't even manage to decode the first macroblock. 
```
$ ffmpeg -i all.h264 -frames:v 1 output.png
left block unavailable for requested intra4x4 mode -1
error while decoding MB 0 0
concealing 660 DC, 660 AC, 660 MV errors in I frame
all.h264: corrupt decoded frame in stream 0
```

The error message comes from [h264_parse.c](https://github.com/FFmpeg/FFmpeg/blob/release/3.2/libavcodec/h264_parse.c#L159). I guess
the data in this very first macroblock claims that it's a delta from the previous (left) block, but that doesn't make sense
since there isn't a previous block!

I don't know where to go next. This is very clearly an IDR slice, but the very first MB in it is nonsensical.
