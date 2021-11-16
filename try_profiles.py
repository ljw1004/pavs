#!/usr/bin/python3
from typing import List
import subprocess
import os

def un(n:int, i:int) -> List[int]:
    """returns a list [0,1,1,0] which has n elements and is the binary expression of i, most significant bit first"""
    r = []
    while n > 0:
        r.insert(0, i % 2)
        i = i >> 1
        n = n - 1
    assert i == 0, "i to big for n"
    return r

def ue(i:int) -> List[int]:
    """Exponential-Golomb code for positive i - https://en.wikipedia.org/wiki/Exponential-Golomb_coding"""
    i = i + 1
    r = []
    while i > 0:
        r.insert(0, i % 2)
        i = i >> 1
    if len(r) == 0:
        r = [0]
    r0 = [0] * (len(r) - 1)
    r0.extend(r)
    return r0

def se(i:int) -> List[int]:
    """Exponential-Golomb code for signed i - https://en.wikipedia.org/wiki/Exponential-Golomb_coding"""
    return ue(-2 * i) if i <= 0 else ue(2*i - 1)

def tobytes(r: List[int]) -> bytearray:
    """given a list of 0/1 bits, constructs a bytearray"""
    buf = bytearray()
    r = r.copy()
    while len(r) % 8 != 0:
        r.append(0)
    while len(r) > 0:
        byte = 0
        for i in range(0,8):
            bit = r.pop(0)
            byte = (byte << 1) + bit
        buf.append(byte)
    return buf

def make_sps(profile_idc: int, level_idc: int) -> bytearray:
    """produces an h.264 SPS"""
    r = []
    r.extend(un(32, 1)) # "00 00 00 01" signals the start of a NAL
    r.extend(un(1, 0)) # u(1) forbidden_zero_bit = 0
    r.extend(un(2, 3)) # u(2) nal_ref_idc = 3
    r.extend(un(5, 7)) # u(5) nal_unit_type = 7
    r.extend(un(8, profile_idc)) # u(8) profile_idc
    r.extend(un(1, 0)) # u(1) constraint_set0_flag
    r.extend(un(1, 0)) # u(1) constraint_set1_flag
    r.extend(un(1, 0)) # u(1) constraint_set2_flag
    r.extend(un(1, 0)) # u(1) constraint_set3_flag
    r.extend(un(1, 0)) # u(1) constraint_set4_flag
    r.extend(un(1, 0)) # u(1) constraint_set5_flag
    r.extend(un(2, 0)) # u(2) reserved_zero_2bits
    r.extend(un(8, level_idc)) # u(8) level_idc
    r.extend(ue(0)) # ue(v) seq_parameter_set_id
    r.extend(ue(0)) # ue(v) log2_max_frame_num_minus4
    r.extend(ue(0)) # ue(v) pic_order_cnt_type
    r.extend(ue(0)) # ue(v) log2_max_pic_order_cnt_lsb_minus4
    r.extend(ue(0)) # ue(v) num_ref_frames
    r.extend(un(1, 0)) # u(1) gaps_in_frame_num_value_allowed_flag
    r.extend(ue(43)) # ue(v) pic_width_in_mbs_minus_1
    r.extend(ue(14)) # ue(v) pic_height_in_map_units_minus_1
    r.extend(un(1, 1)) # u(1) frame_mbs_only_flag
    r.extend(un(1, 0)) # u(1) direct_8x8_inference_flag
    r.extend(un(1,0)) # u(1) frame_cropping_flag
    r.extend(un(1,0)) # u(1) viui_parameters_present_flag
    r.extend(un(1,1)) # u(1) rbsp_stop_one_bit
    return tobytes(r)

def make_pps() -> bytearray:
    """produces an h.264 PPS"""
    r = []
    r.extend(un(32, 1)) # "00 00 00 01" signals the start of a NAL
    r.extend(un(1, 0)) # u(1) forbidden_zero_bit
    r.extend(un(2, 3)) # u(2) nal_ref_idc
    r.extend(un(5, 8)) # u(5) nal_unit_type
    r.extend(ue(0)) # ue(v) pic_parameter_set_id
    r.extend(ue(0)) # ue(v) seq_parameter_set_id
    r.extend(un(1, 0)) # u(1) entropy_coding_mode_flag
    r.extend(un(1,0)) # u(1) bottom_field_pic_order_in_frame_present_flag
    r.extend(ue(0)) # ue(v) num_slice_groups_minus1
    r.extend(ue(0)) # ue(v) num_ref_idx_l0_default_active_minus1
    r.extend(ue(0)) # ue(v) num_ref_idx_l1_default_active_minus1
    r.extend(un(1,0)) # u(1) weighted_pred_flag
    r.extend(un(2,0)) # u(2) weighted_bipred_idc
    r.extend(se(0)) # se(v) pic_init_qp_minus26
    r.extend(se(0)) # se(v) pic_init_qs_minus26
    r.extend(se(0)) # se(v) chroma_qp_index_offset
    r.extend(un(1,0)) # u(1) deblocking_filter_control_present_flag
    r.extend(un(1,0)) # u(1) constrained_intra_pred_flag
    r.extend(un(1,0)) # u(1) redundant_pic_cnt_present_flag
    r.extend(un(1,1)) # u(1) rbsp_stop_one_bit
    return tobytes(r)

with open('frames/frame00000.raw', 'rb') as f:
    psav = bytearray(f.read())
idr = psav[0x240:]

# Here are all the profiles and levels that might be used:
# PROFILES: 66c1, 66, 88, 77, 100, 100c4, 100c45, 110, 122, 244, 110c3, 122c3, 244c3, 44, 83, 83c5, 86, 86c5, 86c3, 128, 118, 134, 135, 138, 139
# LEVELS: 10, 11, 12, 13, 20, 21, 22, 30, 31, 32, 40, 41, 42, 50, 51, 52

for level in [10, 11, 12, 13, 20, 21, 22, 30, 31, 32, 40, 41, 42, 50, 51, 52]:
    for profile in [66, 88, 77, 100, 110, 122, 244, 110, 122, 44, 83, 86, 128, 118, 134, 135, 138, 139]:
        sps = make_sps(profile, level)
        pps = make_pps()
        fn = f'prof{profile}_lev{level}'
        with open(f'h264/{fn}.h264', 'wb') as f:
            f.write(sps)
            f.write(pps)
            f.write(idr)
        r = subprocess.run(['ffmpeg', '-i', f'h264/{fn}.h264', '-c', 'copy', '-bsf:v', 'trace_headers', '-f', 'null', '-'], capture_output=True)
        if r.returncode != 0:
            print(f'*{fn} - we constructed SPS/PPS wrongly')
        else:
            try:
                os.unlink(f'h264/{fn}.png')
            except:
                pass
            r2 = subprocess.run(['ffmpeg', '-i', f'h264/{fn}.h264', '-frames:v', '1', f'h264/{fn}.png'], capture_output=True)
            stderr = r2.stderr.decode()
            if stderr.find('corrupt') == 0:
                print(f'{fn}')
            else:
                os.unlink(f'h264/{fn}.png')
                msg = ''
                if stderr.find('error while decoding MB 0 0'):
                    msg += 'error while decoding MB 0 0. '
                if stderr.find('left block unavailable'):
                    msg += 'left block unavailable. '
                if msg == '':
                    msg = 'corrupt'
                print(f'*{fn} - {msg}')



