import ctypes
from enum import Enum

class LZJ_VERSION(Enum):
    VERSION0 = 0x6C7A6A30 # lzj0
    VERSION1 = 0x6C7A6A31 # lzj1
    VERSION2 = 0x6C7A6A32 # lzj2

class lzj():
    """
    ROM:9FC04910 sub_9FC04910:                            # CODE XREF: sub_9FC02980+D0↑p
    ROM:9FC04910                 move    $a2, $a0
    ROM:9FC04914                 move    $t1, $a1
    ROM:9FC04918                 lbu     $t4, 0($a2)
    ROM:9FC0491C                 addiu   $a2, 1
    ROM:9FC04920                 lbu     $v0, 0($a2)
    ROM:9FC04924                 addiu   $a2, 1
    ROM:9FC04928                 lbu     $v1, 0($a2)
    ROM:9FC0492C                 addiu   $a2, 1
    ROM:9FC04930                 lbu     $a0, 0($a2)
    ROM:9FC04934                 addiu   $a2, 1
    ROM:9FC04938                 move    $t3, $t1
    ROM:9FC0493C                 move    $a3, $zero
    ROM:9FC04940                 move    $t0, $zero
    ROM:9FC04944                 sll     $v0, 8
    ROM:9FC04948                 addu    $t4, $v0
    ROM:9FC0494C                 sll     $v1, 16
    ROM:9FC04950                 addu    $t4, $v1
    ROM:9FC04954                 sll     $a0, 24
    ROM:9FC04958                 addu    $t4, $a0
    ROM:9FC0495C                 addu    $t5, $t1, $t4
    ROM:9FC04960                 sltu    $v0, $t1, $t3
    ROM:9FC04964
    ROM:9FC04964 loc_9FC04964:                            # CODE XREF: sub_9FC04910:loc_9FC04CC4↓j
    ROM:9FC04964                 bnez    $v0, loc_9FC049E8
    ROM:9FC04968                 srl     $t0, 1
    ROM:9FC0496C                 addiu   $t3, $t1, 0x100
    ROM:9FC04970                 bnez    $t0, loc_9FC04984
    ROM:9FC04974                 srl     $a3, 1
    ROM:9FC04978                 li      $t0, 0xFF
    ROM:9FC0497C                 lbu     $a3, 0($a2)
    ROM:9FC04980                 addiu   $a2, 1
    ROM:9FC04984
    ROM:9FC04984 loc_9FC04984:                            # CODE XREF: sub_9FC04910+60↑j
    ROM:9FC04984                 andi    $v0, $a3, 1
    ROM:9FC04988                 beqz    $v0, loc_9FC04CC0
    ROM:9FC0498C                 sltu    $v0, $t1, $t3
    ROM:9FC04990                 beqz    $v0, loc_9FC04CC4
    ROM:9FC04994                 sltu    $v0, $t1, $t5
    ROM:9FC04998
    ROM:9FC04998 loc_9FC04998:                            # CODE XREF: sub_9FC04910+C8↓j
    ROM:9FC04998                 lbu     $v0, 0($a2)
    ROM:9FC0499C                 addiu   $a2, 1
    ROM:9FC049A0                 lbu     $v1, 0($a2)
    ROM:9FC049A4                 addiu   $a2, 1
    ROM:9FC049A8                 lbu     $a0, 0($a2)
    ROM:9FC049AC                 addiu   $a2, 1
    ROM:9FC049B0                 lbu     $a1, 0($a2)
    ROM:9FC049B4                 sb      $v0, 0($t1)
    ROM:9FC049B8                 addiu   $t1, 1
    ROM:9FC049BC                 sb      $v1, 0($t1)
    ROM:9FC049C0                 addiu   $t1, 1
    ROM:9FC049C4                 sb      $a0, 0($t1)
    ROM:9FC049C8                 addiu   $t1, 1
    ROM:9FC049CC                 sb      $a1, 0($t1)
    ROM:9FC049D0                 addiu   $t1, 1
    ROM:9FC049D4                 sltu    $v0, $t1, $t3
    ROM:9FC049D8                 bnez    $v0, loc_9FC04998
    ROM:9FC049DC                 addiu   $a2, 1
    ROM:9FC049E0                 j       loc_9FC04CC4
    ROM:9FC049E4                 sltu    $v0, $t1, $t5
    ROM:9FC049E8  # ---------------------------------------------------------------------------
    ROM:9FC049E8
    ROM:9FC049E8 loc_9FC049E8:                            # CODE XREF: sub_9FC04910:loc_9FC04964↑j
    ROM:9FC049E8                 bnez    $t0, loc_9FC049FC
    ROM:9FC049EC                 srl     $a3, 1
    ROM:9FC049F0                 li      $t0, 0xFF
    ROM:9FC049F4                 lbu     $a3, 0($a2)
    ROM:9FC049F8                 addiu   $a2, 1
    ROM:9FC049FC
    ROM:9FC049FC loc_9FC049FC:                            # CODE XREF: sub_9FC04910:loc_9FC049E8↑j
    ROM:9FC049FC                 andi    $v0, $a3, 1
    ROM:9FC04A00                 beqzl   $v0, loc_9FC04A1C
    ROM:9FC04A04                 srl     $t0, 1
    ROM:9FC04A08                 lbu     $v0, 0($a2)
    ROM:9FC04A0C                 addiu   $a2, 1
    ROM:9FC04A10                 sb      $v0, 0($t1)
    ROM:9FC04A14                 j       loc_9FC04CC0
    ROM:9FC04A18                 addiu   $t1, 1
    ROM:9FC04A1C  # ---------------------------------------------------------------------------
    ROM:9FC04A1C
    ROM:9FC04A1C loc_9FC04A1C:                            # CODE XREF: sub_9FC04910+F0↑j
    ROM:9FC04A1C                 bnez    $t0, loc_9FC04A30
    ROM:9FC04A20                 srl     $a3, 1
    ROM:9FC04A24                 li      $t0, 0xFF
    ROM:9FC04A28                 lbu     $a3, 0($a2)
    ROM:9FC04A2C                 addiu   $a2, 1
    ROM:9FC04A30
    ROM:9FC04A30 loc_9FC04A30:                            # CODE XREF: sub_9FC04910:loc_9FC04A1C↑j
    ROM:9FC04A30                 andi    $v0, $a3, 1
    ROM:9FC04A34                 bnez    $v0, loc_9FC04B28
    ROM:9FC04A38                 srl     $t0, 1
    ROM:9FC04A3C                 bnez    $t0, loc_9FC04A50
    ROM:9FC04A40                 srl     $a3, 1
    ROM:9FC04A44                 li      $t0, 0xFF
    ROM:9FC04A48                 lbu     $a3, 0($a2)
    ROM:9FC04A4C                 addiu   $a2, 1
    ROM:9FC04A50
    ROM:9FC04A50 loc_9FC04A50:                            # CODE XREF: sub_9FC04910+12C↑j
    ROM:9FC04A50                 andi    $v0, $a3, 1
    ROM:9FC04A54                 bnez    $v0, loc_9FC04AB4
    ROM:9FC04A58                 li      $t2, 4
    ROM:9FC04A5C                 srl     $t0, 1
    ROM:9FC04A60                 bnez    $t0, loc_9FC04A74
    ROM:9FC04A64                 srl     $a3, 1
    ROM:9FC04A68                 li      $t0, 0xFF
    ROM:9FC04A6C                 lbu     $a3, 0($a2)
    ROM:9FC04A70                 addiu   $a2, 1
    ROM:9FC04A74
    ROM:9FC04A74 loc_9FC04A74:                            # CODE XREF: sub_9FC04910+150↑j
    ROM:9FC04A74                 andi    $v0, $a3, 1
    ROM:9FC04A78                 bnez    $v0, loc_9FC04A88
    ROM:9FC04A7C                 li      $t2, 3
    ROM:9FC04A80                 j       loc_9FC04BE8
    ROM:9FC04A84                 li      $t2, 2
    ROM:9FC04A88  # ---------------------------------------------------------------------------
    ROM:9FC04A88
    ROM:9FC04A88 loc_9FC04A88:                            # CODE XREF: sub_9FC04910+168↑j
    ROM:9FC04A88                 srl     $t0, 1
    ROM:9FC04A8C                 bnez    $t0, loc_9FC04AA0
    ROM:9FC04A90                 srl     $a3, 1
    ROM:9FC04A94                 li      $t0, 0xFF
    ROM:9FC04A98                 lbu     $a3, 0($a2)
    ROM:9FC04A9C                 addiu   $a2, 1
    ROM:9FC04AA0
    ROM:9FC04AA0 loc_9FC04AA0:                            # CODE XREF: sub_9FC04910+17C↑j
    ROM:9FC04AA0                 andi    $v0, $a3, 1
    ROM:9FC04AA4                 beqz    $v0, loc_9FC04BEC
    ROM:9FC04AA8                 li      $a1, 1
    ROM:9FC04AAC                 j       loc_9FC04C50
    ROM:9FC04AB0                 li      $a1, 0x101
    ROM:9FC04AB4  # ---------------------------------------------------------------------------
    ROM:9FC04AB4
    ROM:9FC04AB4 loc_9FC04AB4:                            # CODE XREF: sub_9FC04910+144↑j
    ROM:9FC04AB4                 srl     $t0, 1
    ROM:9FC04AB8                 bnez    $t0, loc_9FC04ACC
    ROM:9FC04ABC                 srl     $a3, 1
    ROM:9FC04AC0                 li      $t0, 0xFF
    ROM:9FC04AC4                 lbu     $a3, 0($a2)
    ROM:9FC04AC8                 addiu   $a2, 1
    ROM:9FC04ACC
    ROM:9FC04ACC loc_9FC04ACC:                            # CODE XREF: sub_9FC04910+1A8↑j
    ROM:9FC04ACC                 andi    $v0, $a3, 1
    ROM:9FC04AD0                 bnez    $v0, loc_9FC04B00
    ROM:9FC04AD4                 srl     $t0, 1
    ROM:9FC04AD8                 bnez    $t0, loc_9FC04AEC
    ROM:9FC04ADC                 srl     $a3, 1
    ROM:9FC04AE0                 li      $t0, 0xFF
    ROM:9FC04AE4                 lbu     $a3, 0($a2)
    ROM:9FC04AE8                 addiu   $a2, 1
    ROM:9FC04AEC
    ROM:9FC04AEC loc_9FC04AEC:                            # CODE XREF: sub_9FC04910+1C8↑j
    ROM:9FC04AEC                 andi    $v0, $a3, 1
    ROM:9FC04AF0                 beqz    $v0, loc_9FC04BEC
    ROM:9FC04AF4                 li      $a1, 1
    ROM:9FC04AF8                 j       loc_9FC04C50
    ROM:9FC04AFC                 li      $a1, 0x101
    ROM:9FC04B00  # ---------------------------------------------------------------------------
    ROM:9FC04B00
    ROM:9FC04B00 loc_9FC04B00:                            # CODE XREF: sub_9FC04910+1C0↑j
    ROM:9FC04B00                 bnez    $t0, loc_9FC04B14
    ROM:9FC04B04                 srl     $a3, 1
    ROM:9FC04B08                 li      $t0, 0xFF
    ROM:9FC04B0C                 lbu     $a3, 0($a2)
    ROM:9FC04B10                 addiu   $a2, 1
    ROM:9FC04B14
    ROM:9FC04B14 loc_9FC04B14:                            # CODE XREF: sub_9FC04910:loc_9FC04B00↑j
    ROM:9FC04B14                 andi    $v0, $a3, 1
    ROM:9FC04B18                 beqz    $v0, loc_9FC04BF4
    ROM:9FC04B1C                 li      $a1, 0x1101
    ROM:9FC04B20                 j       loc_9FC04C20
    ROM:9FC04B24                 lui     $a1, 1
    ROM:9FC04B28  # ---------------------------------------------------------------------------
    ROM:9FC04B28
    ROM:9FC04B28 loc_9FC04B28:                            # CODE XREF: sub_9FC04910+124↑j
    ROM:9FC04B28                 bnez    $t0, loc_9FC04B3C
    ROM:9FC04B2C                 srl     $a3, 1
    ROM:9FC04B30                 li      $t0, 0xFF
    ROM:9FC04B34                 lbu     $a3, 0($a2)
    ROM:9FC04B38                 addiu   $a2, 1
    ROM:9FC04B3C
    ROM:9FC04B3C loc_9FC04B3C:                            # CODE XREF: sub_9FC04910:loc_9FC04B28↑j
    ROM:9FC04B3C                 andi    $v0, $a3, 1
    ROM:9FC04B40                 bnez    $v0, loc_9FC04B98
    ROM:9FC04B44                 li      $t2, 5
    ROM:9FC04B48                 srl     $t0, 1
    ROM:9FC04B4C                 bnez    $t0, loc_9FC04B60
    ROM:9FC04B50                 srl     $a3, 1
    ROM:9FC04B54                 li      $t0, 0xFF
    ROM:9FC04B58                 lbu     $a3, 0($a2)
    ROM:9FC04B5C                 addiu   $a2, 1
    ROM:9FC04B60
    ROM:9FC04B60 loc_9FC04B60:                            # CODE XREF: sub_9FC04910+23C↑j
    ROM:9FC04B60                 andi    $v0, $a3, 1
    ROM:9FC04B64                 bnezl   $v0, loc_9FC04B6C
    ROM:9FC04B68                 li      $t2, 7
    ROM:9FC04B6C
    ROM:9FC04B6C loc_9FC04B6C:                            # CODE XREF: sub_9FC04910+254↑j
    ROM:9FC04B6C                 srl     $t0, 1
    ROM:9FC04B70                 bnez    $t0, loc_9FC04B84
    ROM:9FC04B74                 srl     $a3, 1
    ROM:9FC04B78                 li      $t0, 0xFF
    ROM:9FC04B7C                 lbu     $a3, 0($a2)
    ROM:9FC04B80                 addiu   $a2, 1
    ROM:9FC04B84
    ROM:9FC04B84 loc_9FC04B84:                            # CODE XREF: sub_9FC04910+260↑j
    ROM:9FC04B84                 andi    $v0, $a3, 1
    ROM:9FC04B88                 bnezl   $v0, loc_9FC04BA4
    ROM:9FC04B8C                 addiu   $t2, 1
    ROM:9FC04B90                 j       loc_9FC04BA8
    ROM:9FC04B94                 srl     $t0, 1
    ROM:9FC04B98  # ---------------------------------------------------------------------------
    ROM:9FC04B98
    ROM:9FC04B98 loc_9FC04B98:                            # CODE XREF: sub_9FC04910+230↑j
    ROM:9FC04B98                 lbu     $v0, 0($a2)
    ROM:9FC04B9C                 addiu   $a2, 1
    ROM:9FC04BA0                 addiu   $t2, $v0, 9
    ROM:9FC04BA4
    ROM:9FC04BA4 loc_9FC04BA4:                            # CODE XREF: sub_9FC04910+278↑j
    ROM:9FC04BA4                 srl     $t0, 1
    ROM:9FC04BA8
    ROM:9FC04BA8 loc_9FC04BA8:                            # CODE XREF: sub_9FC04910+280↑j
    ROM:9FC04BA8                 bnez    $t0, loc_9FC04BBC
    ROM:9FC04BAC                 srl     $a3, 1
    ROM:9FC04BB0                 li      $t0, 0xFF
    ROM:9FC04BB4                 lbu     $a3, 0($a2)
    ROM:9FC04BB8                 addiu   $a2, 1
    ROM:9FC04BBC
    ROM:9FC04BBC loc_9FC04BBC:                            # CODE XREF: sub_9FC04910:loc_9FC04BA8↑j
    ROM:9FC04BBC                 andi    $v0, $a3, 1
    ROM:9FC04BC0                 bnez    $v0, loc_9FC04BFC
    ROM:9FC04BC4                 srl     $t0, 1
    ROM:9FC04BC8                 bnez    $t0, loc_9FC04BDC
    ROM:9FC04BCC                 srl     $a3, 1
    ROM:9FC04BD0                 li      $t0, 0xFF
    ROM:9FC04BD4                 lbu     $a3, 0($a2)
    ROM:9FC04BD8                 addiu   $a2, 1
    ROM:9FC04BDC
    ROM:9FC04BDC loc_9FC04BDC:                            # CODE XREF: sub_9FC04910+2B8↑j
    ROM:9FC04BDC                 andi    $v0, $a3, 1
    ROM:9FC04BE0                 bnez    $v0, loc_9FC04BF4
    ROM:9FC04BE4                 li      $a1, 0x1101
    ROM:9FC04BE8
    ROM:9FC04BE8 loc_9FC04BE8:                            # CODE XREF: sub_9FC04910+170↑j
    ROM:9FC04BE8                 li      $a1, 1
    ROM:9FC04BEC
    ROM:9FC04BEC loc_9FC04BEC:                            # CODE XREF: sub_9FC04910+194↑j
    ROM:9FC04BEC                                          # sub_9FC04910+1E0↑j
    ROM:9FC04BEC                 j       loc_9FC04C60
    ROM:9FC04BF0                 li      $v1, 8
    ROM:9FC04BF4  # ---------------------------------------------------------------------------
    ROM:9FC04BF4
    ROM:9FC04BF4 loc_9FC04BF4:                            # CODE XREF: sub_9FC04910+208↑j
    ROM:9FC04BF4                                          # sub_9FC04910+2D0↑j
    ROM:9FC04BF4                 j       loc_9FC04C60
    ROM:9FC04BF8                 li      $v1, 0x10
    ROM:9FC04BFC  # ---------------------------------------------------------------------------
    ROM:9FC04BFC
    ROM:9FC04BFC loc_9FC04BFC:                            # CODE XREF: sub_9FC04910+2B0↑j
    ROM:9FC04BFC                 bnez    $t0, loc_9FC04C10
    ROM:9FC04C00                 srl     $a3, 1
    ROM:9FC04C04                 li      $t0, 0xFF
    ROM:9FC04C08                 lbu     $a3, 0($a2)
    ROM:9FC04C0C                 addiu   $a2, 1
    ROM:9FC04C10
    ROM:9FC04C10 loc_9FC04C10:                            # CODE XREF: sub_9FC04910:loc_9FC04BFC↑j
    ROM:9FC04C10                 andi    $v0, $a3, 1
    ROM:9FC04C14                 bnezl   $v0, loc_9FC04C2C
    ROM:9FC04C18                 srl     $t0, 1
    ROM:9FC04C1C                 lui     $a1, 1
    ROM:9FC04C20
    ROM:9FC04C20 loc_9FC04C20:                            # CODE XREF: sub_9FC04910+210↑j
    ROM:9FC04C20                 ori     $a1, 0x1101
    ROM:9FC04C24                 j       loc_9FC04C60
    ROM:9FC04C28                 li      $v1, 0x14
    ROM:9FC04C2C  # ---------------------------------------------------------------------------
    ROM:9FC04C2C
    ROM:9FC04C2C loc_9FC04C2C:                            # CODE XREF: sub_9FC04910+304↑j
    ROM:9FC04C2C                 bnez    $t0, loc_9FC04C40
    ROM:9FC04C30                 srl     $a3, 1
    ROM:9FC04C34                 li      $t0, 0xFF
    ROM:9FC04C38                 lbu     $a3, 0($a2)
    ROM:9FC04C3C                 addiu   $a2, 1
    ROM:9FC04C40
    ROM:9FC04C40 loc_9FC04C40:                            # CODE XREF: sub_9FC04910:loc_9FC04C2C↑j
    ROM:9FC04C40                 andi    $v0, $a3, 1
    ROM:9FC04C44                 bnez    $v0, loc_9FC04C58
    ROM:9FC04C48                 lui     $a1, 0x11
    ROM:9FC04C4C                 li      $a1, 0x101
    ROM:9FC04C50
    ROM:9FC04C50 loc_9FC04C50:                            # CODE XREF: sub_9FC04910+19C↑j
    ROM:9FC04C50                                          # sub_9FC04910+1E8↑j
    ROM:9FC04C50                 j       loc_9FC04C60
    ROM:9FC04C54                 li      $v1, 0xC
    ROM:9FC04C58  # ---------------------------------------------------------------------------
    ROM:9FC04C58
    ROM:9FC04C58 loc_9FC04C58:                            # CODE XREF: sub_9FC04910+334↑j
    ROM:9FC04C58                 ori     $a1, 0x1101
    ROM:9FC04C5C                 li      $v1, 0x17
    ROM:9FC04C60
    ROM:9FC04C60 loc_9FC04C60:                            # CODE XREF: sub_9FC04910:loc_9FC04BEC↑j
    ROM:9FC04C60                                          # sub_9FC04910:loc_9FC04BF4↑j ...
    ROM:9FC04C60                 move    $a0, $zero
    ROM:9FC04C64
    ROM:9FC04C64 loc_9FC04C64:                            # CODE XREF: sub_9FC04910+378↓j
    ROM:9FC04C64                 srl     $t0, 1
    ROM:9FC04C68                 bnez    $t0, loc_9FC04C7C
    ROM:9FC04C6C                 srl     $a3, 1
    ROM:9FC04C70                 li      $t0, 0xFF
    ROM:9FC04C74                 lbu     $a3, 0($a2)
    ROM:9FC04C78                 addiu   $a2, 1
    ROM:9FC04C7C
    ROM:9FC04C7C loc_9FC04C7C:                            # CODE XREF: sub_9FC04910+358↑j
    ROM:9FC04C7C                 sll     $a0, 1
    ROM:9FC04C80                 andi    $v0, $a3, 1
    ROM:9FC04C84                 addiu   $v1, -1
    ROM:9FC04C88                 bnez    $v1, loc_9FC04C64
    ROM:9FC04C8C                 addu    $a0, $v0
    ROM:9FC04C90                 subu    $v0, $t1, $a1
    ROM:9FC04C94                 subu    $v1, $v0, $a0
    ROM:9FC04C98                 addu    $v0, $v1, $t2
    ROM:9FC04C9C                 sltu    $v0, $t5, $v0
    ROM:9FC04CA0                 bnezl   $v0, loc_9FC04CA8
    ROM:9FC04CA4                 subu    $t2, $t5, $v1
    ROM:9FC04CA8
    ROM:9FC04CA8 loc_9FC04CA8:                            # CODE XREF: sub_9FC04910+390↑j
    ROM:9FC04CA8                                          # sub_9FC04910+3A8↓j
    ROM:9FC04CA8                 lbu     $v0, 0($v1)
    ROM:9FC04CAC                 addiu   $v1, 1
    ROM:9FC04CB0                 addiu   $t2, -1
    ROM:9FC04CB4                 sb      $v0, 0($t1)
    ROM:9FC04CB8                 bnez    $t2, loc_9FC04CA8
    ROM:9FC04CBC                 addiu   $t1, 1
    ROM:9FC04CC0
    ROM:9FC04CC0 loc_9FC04CC0:                            # CODE XREF: sub_9FC04910+78↑j
    ROM:9FC04CC0                                          # sub_9FC04910+104↑j
    ROM:9FC04CC0                 sltu    $v0, $t1, $t5
    ROM:9FC04CC4
    ROM:9FC04CC4 loc_9FC04CC4:                            # CODE XREF: sub_9FC04910+80↑j
    ROM:9FC04CC4                                          # sub_9FC04910+D0↑j
    ROM:9FC04CC4                 bnezl   $v0, loc_9FC04964
    ROM:9FC04CC8                 sltu    $v0, $t1, $t3
    ROM:9FC04CCC                 jr      $ra
    ROM:9FC04CD0                 move    $v0, $t4
    ROM:9FC04CD0  # End of function sub_9FC04910
    """
    def ExpandLzj(data, version: LZJ_VERSION = LZJ_VERSION.VERSION1):
        uncompressed_size = int.from_bytes(data[0:4], "little")

        uncompressed_data = bytearray(uncompressed_size)

        cool1 = 0
        cool2 = 0
        cool3 = 0
        cool4 = 0
        cool5 = 0
        cool6 = 0x100
        cool7 = 0
        cool8 = 0
        i = 4
        r = 0

        if version == LZJ_VERSION.VERSION2:
            cool6 = 0
        else:
            cool6 = 0x100

        def _add_byte(byte):
            nonlocal r

            uncompressed_data[r] = byte
            r += 1

        def _copy_bytes(size):
            nonlocal r, i

            for p in range(size):
                _add_byte(data[i])
                i += 1
        
        def _next():
            nonlocal data, i, cool1, cool2

            is_odd = ((cool1 & 1) == 1)

            cool1 >>= 1
            cool2 >>= 1

            if cool2 == 0:
                if i >= len(data):
                    cool1 = 0x00
                else:
                    cool1 = data[i]
                i += 1
                cool2 = 0xFF

            return is_odd

        while uncompressed_size > r:
            neat = 0x00

            _next()

            if cool3 == 0 or r >= cool3:
                cool3 = r + 0x100

                if (cool1 & 1) == 1:
                    while r < cool3:
                        _copy_bytes(4)
            elif (cool1 & 1) == 1:
                _copy_bytes(1)
            else:
                _next()
                
                if _next():
                    neat = 0x05

                    if (cool1 & 1) == 1:
                        neat = data[i] + 0x09
                        i += 1
                    else:
                        _next()

                        if (cool1 & 1) == 1:
                            neat = 0x07

                        _next()

                        if (cool1 & 1) == 1:
                            neat += 0x01

                    _next()

                    if _next():
                        if (cool1 & 1) == 1:
                            if version != LZJ_VERSION.VERSION2 or r > 0x111001:
                                _next()

                                if (cool1 & 1) == 1:
                                    cool4 = cool6 + 0x111001
                                    cool5 = 0x17
                                else:
                                    cool4 = cool6 + 0x01
                                    cool5 = 0x0c
                            else:
                                cool4 = cool6 + 0x01
                                cool5 = 0x0c

                        else:
                            cool4 = cool6 + 0x11001
                            cool5 = 0x14
                    else:
                        if (cool1 & 1) == 1:
                            cool4 = cool6 + 0x1001
                            cool5 = 0x10
                        else:
                            cool4 = 1
                            cool5 = 8
                else:
                    if _next():
                        neat = 0x04

                        if _next():
                            if (cool1 & 1) == 1:
                                cool4 = cool6 + 0x11001
                                cool5 = 0x14
                            else:
                                cool4 = cool6 + 0x1001
                                cool5 = 0x10
                        else:
                            if (cool1 & 1) == 1:
                                cool4 = cool6 + 0x01
                                cool5 = 0x0c
                            else:
                                cool4 = 1
                                cool5 = 8
                    else:
                        if (cool1 & 1) == 1:
                            neat = 0x03

                            _next()

                            if version == LZJ_VERSION.VERSION0:
                                if (cool1 & 1) == 1:
                                    cool4 = cool6 + 0x1001
                                    cool5 = 0x10
                                else:
                                    _next()

                                    if (cool1 & 1) == 1:
                                        cool4 = cool6 + 0x01
                                        cool5 = 0x0c
                                    else:
                                        cool4 = 1
                                        cool5 = 8
                            else:
                                if (cool1 & 1) == 1:
                                    cool4 = cool6 + 0x01
                                    cool5 = 0x0c
                                else:
                                    cool4 = 1
                                    cool5 = 8
                        else:
                            neat = 0x02

                            cool4 = 1
                            cool5 = 8

                _cool5 = cool5
                stop_early = (version == LZJ_VERSION.VERSION2 and cool5 == 0x0c)
                cool7 = 0
                while cool5 != 0:
                    _next()
                    cool7 = (cool7 * 2) + (cool1 & 1)
                    cool5 -= 1

                    if cool5 <= 0x08 and stop_early:
                        if cool7 != 0:
                            stop_early = False
                        else:
                            break

                if not stop_early:
                    cool8 = (cool4 + cool7)

                cool9 = r - cool8

                if uncompressed_size < (cool9 + neat):
                    neat = uncompressed_size - cool9
                elif cool9 > r:
                    print("\tBORKED [" + hex(cool9) + " > " + hex(r) + "]! Returning, stopped at offset " + hex(i))

                    break
                elif cool9 < 0:
                    print("\tBORKED [" + hex(cool9) + " < 0x00]! Returning, stopped at offset " + hex(i))

                    break

                while neat != 0:
                    _add_byte(uncompressed_data[cool9])
                    cool9 += 1

                    neat -= 1

        print("i", hex(i))
        return uncompressed_data


    """
    ROM:8021F1A4 ExpandLzj:                               # CODE XREF: LoadBrowserImage+E0↑p
    ROM:8021F1A4                 addiu   $sp, -0x460
    ROM:8021F1A8                 sw      $s5, 0x44C($sp)
    ROM:8021F1AC                 li      $s5, 0x100
    ROM:8021F1B0                 li      $v0, 0x6C7A6A30
    ROM:8021F1B8                 sw      $ra, 0x45C($sp)
    ROM:8021F1BC                 sw      $fp, 0x458($sp)
    ROM:8021F1C0                 sw      $s7, 0x454($sp)
    ROM:8021F1C4                 sw      $s6, 0x450($sp)
    ROM:8021F1C8                 sw      $s4, 0x448($sp)
    ROM:8021F1CC                 sw      $s3, 0x444($sp)
    ROM:8021F1D0                 sw      $s2, 0x440($sp)
    ROM:8021F1D4                 sw      $s1, 0x43C($sp)
    ROM:8021F1D8                 sw      $s0, 0x438($sp)
    ROM:8021F1DC                 sw      $a0, 0x414($sp)
    ROM:8021F1E0                 bne     $a2, $v0, loc_8021F1F0
    ROM:8021F1E4                 sw      $a1, 0x41C($sp)
    ROM:8021F1E8                 j       loc_8021F240
    ROM:8021F1EC                 sw      $zero, 0x434($sp)
    ROM:8021F1F0  # ---------------------------------------------------------------------------
    ROM:8021F1F0
    ROM:8021F1F0 loc_8021F1F0:                            # CODE XREF: ExpandLzj+3C↑j
    ROM:8021F1F0                 li      $v0, 0x6C7A6A31
    ROM:8021F1F8                 bne     $a2, $v0, loc_8021F20C
    ROM:8021F1FC                 lui     $v0, 0x6C7A
    ROM:8021F200                 li      $t0, 1
    ROM:8021F204                 j       loc_8021F240
    ROM:8021F208                 sw      $t0, 0x434($sp)
    ROM:8021F20C  # ---------------------------------------------------------------------------
    ROM:8021F20C
    ROM:8021F20C loc_8021F20C:                            # CODE XREF: ExpandLzj+54↑j
    ROM:8021F20C                 ori     $v0, 0x6A32
    ROM:8021F210                 beq     $a2, $v0, loc_8021F238
    ROM:8021F214                 li      $t0, 2
    ROM:8021F218                 lui     $a0, 0x8038
    ROM:8021F21C                 jal     DisplayMessage
    ROM:8021F220                 la      $a0, 0x80386314  # "Unrecognized lzj version - update your "...
    ROM:8021F224                 lui     $a0, 0x8038
    ROM:8021F228                 jal     DisplayMessage
    ROM:8021F22C                 la      $a0, asc_80385E9C  # "\n"
    ROM:8021F230                 j       loc_8021F778
    ROM:8021F234                 move    $v0, $zero
    ROM:8021F238  # ---------------------------------------------------------------------------
    ROM:8021F238
    ROM:8021F238 loc_8021F238:                            # CODE XREF: ExpandLzj+6C↑j
    ROM:8021F238                 sw      $t0, 0x434($sp)
    ROM:8021F23C                 move    $s5, $zero
    ROM:8021F240
    ROM:8021F240 loc_8021F240:                            # CODE XREF: ExpandLzj+44↑j
    ROM:8021F240                                          # ExpandLzj+60↑j
    ROM:8021F240                 addiu   $a0, $sp, 0x10
    ROM:8021F244                 lw      $t0, 0x414($sp)
    ROM:8021F248                 jalr    $t0
    ROM:8021F24C                 li      $a1, 0x200
    ROM:8021F250                 addiu   $v1, $sp, 0x10
    ROM:8021F254                 addu    $s4, $v1, $v0
    ROM:8021F258                 addiu   $s0, $sp, 0x14
    ROM:8021F25C                 move    $s1, $zero
    ROM:8021F260                 move    $s6, $v1
    ROM:8021F264                 lw      $s3, 0x41C($sp)
    ROM:8021F268                 lbu     $v0, 0x11($sp)
    ROM:8021F26C                 lbu     $fp, 0x10($sp)
    ROM:8021F270                 lbu     $v1, 0x12($sp)
    ROM:8021F274                 move    $s2, $zero
    ROM:8021F278                 sw      $zero, 0x42C($sp)
    ROM:8021F27C                 move    $s7, $s3
    ROM:8021F280                 sll     $v0, 8
    ROM:8021F284                 addu    $fp, $v0
    ROM:8021F288                 sll     $v1, 16
    ROM:8021F28C                 lbu     $v0, 0x13($sp)
    ROM:8021F290                 addu    $fp, $v1
    ROM:8021F294                 sll     $v0, 24
    ROM:8021F298                 addu    $fp, $v0
    ROM:8021F29C                 addu    $t0, $s3, $fp
    ROM:8021F2A0                 sw      $t0, 0x424($sp)
    ROM:8021F2A4                 addiu   $v0, $s0, 4
    ROM:8021F2A8
    ROM:8021F2A8 loc_8021F2A8:                            # CODE XREF: ExpandLzj+5C8↓j
    ROM:8021F2A8                 sltu    $v0, $s4
    ROM:8021F2AC                 bnez    $v0, loc_8021F2F8
    ROM:8021F2B0                 sltu    $v0, $s3, $s7
    ROM:8021F2B4                 subu    $v0, $s0, $s6
    ROM:8021F2B8                 subu    $s4, $v0
    ROM:8021F2BC                 lbu     $v0, 0($s0)
    ROM:8021F2C0                 lbu     $v1, 1($s0)
    ROM:8021F2C4                 lbu     $a2, 2($s0)
    ROM:8021F2C8                 lbu     $a3, 3($s0)
    ROM:8021F2CC                 move    $s0, $s6
    ROM:8021F2D0                 move    $a0, $s4
    ROM:8021F2D4                 lw      $t0, 0x414($sp)
    ROM:8021F2D8                 li      $a1, 0x200
    ROM:8021F2DC                 sb      $v0, 0x10($sp)
    ROM:8021F2E0                 sb      $v1, 0x11($sp)
    ROM:8021F2E4                 sb      $a2, 0x12($sp)
    ROM:8021F2E8                 jalr    $t0
    ROM:8021F2EC                 sb      $a3, 0x13($sp)
    ROM:8021F2F0                 addu    $s4, $v0
    ROM:8021F2F4                 sltu    $v0, $s3, $s7
    ROM:8021F2F8
    ROM:8021F2F8 loc_8021F2F8:                            # CODE XREF: ExpandLzj+108↑j
    ROM:8021F2F8                 bnez    $v0, loc_8021F3C8
    ROM:8021F2FC                 srl     $s2, 1
    ROM:8021F300                 addiu   $s7, $s3, 0x100
    ROM:8021F304                 bnez    $s2, loc_8021F318
    ROM:8021F308                 srl     $s1, 1
    ROM:8021F30C                 li      $s2, 0xFF
    ROM:8021F310                 lbu     $s1, 0($s0)
    ROM:8021F314                 addiu   $s0, 1
    ROM:8021F318
    ROM:8021F318 loc_8021F318:                            # CODE XREF: ExpandLzj+160↑j
    ROM:8021F318                 andi    $v0, $s1, 1
    ROM:8021F31C                 beqz    $v0, loc_8021F764
    ROM:8021F320                 sltu    $v0, $s3, $s7
    ROM:8021F324                 beqz    $v0, loc_8021F764
    ROM:8021F328                 nop
    ROM:8021F32C
    ROM:8021F32C loc_8021F32C:                            # CODE XREF: ExpandLzj+214↓j
    ROM:8021F32C                 addiu   $v0, $s0, 4
    ROM:8021F330                 sltu    $v0, $s4
    ROM:8021F334                 bnez    $v0, loc_8021F378
    ROM:8021F338                 subu    $v0, $s0, $s6
    ROM:8021F33C                 subu    $s4, $v0
    ROM:8021F340                 lbu     $v0, 0($s0)
    ROM:8021F344                 lbu     $v1, 1($s0)
    ROM:8021F348                 lbu     $a2, 2($s0)
    ROM:8021F34C                 lbu     $a3, 3($s0)
    ROM:8021F350                 move    $s0, $s6
    ROM:8021F354                 move    $a0, $s4
    ROM:8021F358                 lw      $t0, 0x414($sp)
    ROM:8021F35C                 li      $a1, 0x200
    ROM:8021F360                 sb      $v0, 0x10($sp)
    ROM:8021F364                 sb      $v1, 0x11($sp)
    ROM:8021F368                 sb      $a2, 0x12($sp)
    ROM:8021F36C                 jalr    $t0
    ROM:8021F370                 sb      $a3, 0x13($sp)
    ROM:8021F374                 addu    $s4, $v0
    ROM:8021F378
    ROM:8021F378 loc_8021F378:                            # CODE XREF: ExpandLzj+190↑j
    ROM:8021F378                 lbu     $v0, 0($s0)
    ROM:8021F37C                 addiu   $s0, 1
    ROM:8021F380                 lbu     $v1, 0($s0)
    ROM:8021F384                 addiu   $s0, 1
    ROM:8021F388                 lbu     $a0, 0($s0)
    ROM:8021F38C                 addiu   $s0, 1
    ROM:8021F390                 lbu     $a1, 0($s0)
    ROM:8021F394                 sb      $v0, 0($s3)
    ROM:8021F398                 addiu   $s3, 1
    ROM:8021F39C                 sb      $v1, 0($s3)
    ROM:8021F3A0                 addiu   $s3, 1
    ROM:8021F3A4                 sb      $a0, 0($s3)
    ROM:8021F3A8                 addiu   $s3, 1
    ROM:8021F3AC                 sb      $a1, 0($s3)
    ROM:8021F3B0                 addiu   $s3, 1
    ROM:8021F3B4                 sltu    $v0, $s3, $s7
    ROM:8021F3B8                 bnez    $v0, loc_8021F32C
    ROM:8021F3BC                 addiu   $s0, 1
    ROM:8021F3C0                 j       loc_8021F764
    ROM:8021F3C4                 nop
    ROM:8021F3C8  # ---------------------------------------------------------------------------
    ROM:8021F3C8
    ROM:8021F3C8 loc_8021F3C8:                            # CODE XREF: ExpandLzj:loc_8021F2F8↑j
    ROM:8021F3C8                 bnez    $s2, loc_8021F3DC
    ROM:8021F3CC                 srl     $s1, 1
    ROM:8021F3D0                 li      $s2, 0xFF
    ROM:8021F3D4                 lbu     $s1, 0($s0)
    ROM:8021F3D8                 addiu   $s0, 1
    ROM:8021F3DC
    ROM:8021F3DC loc_8021F3DC:                            # CODE XREF: ExpandLzj:loc_8021F3C8↑j
    ROM:8021F3DC                 andi    $v0, $s1, 1
    ROM:8021F3E0                 beqzl   $v0, loc_8021F3FC
    ROM:8021F3E4                 srl     $s2, 1
    ROM:8021F3E8                 lbu     $v0, 0($s0)
    ROM:8021F3EC                 addiu   $s0, 1
    ROM:8021F3F0                 sb      $v0, 0($s3)
    ROM:8021F3F4                 j       loc_8021F764
    ROM:8021F3F8                 addiu   $s3, 1
    ROM:8021F3FC  # ---------------------------------------------------------------------------
    ROM:8021F3FC
    ROM:8021F3FC loc_8021F3FC:                            # CODE XREF: ExpandLzj+23C↑j
    ROM:8021F3FC                 bnez    $s2, loc_8021F410
    ROM:8021F400                 srl     $s1, 1
    ROM:8021F404                 li      $s2, 0xFF
    ROM:8021F408                 lbu     $s1, 0($s0)
    ROM:8021F40C                 addiu   $s0, 1
    ROM:8021F410
    ROM:8021F410 loc_8021F410:                            # CODE XREF: ExpandLzj:loc_8021F3FC↑j
    ROM:8021F410                 andi    $v0, $s1, 1
    ROM:8021F414                 bnez    $v0, loc_8021F510
    ROM:8021F418                 srl     $s2, 1
    ROM:8021F41C                 bnez    $s2, loc_8021F430
    ROM:8021F420                 srl     $s1, 1
    ROM:8021F424                 li      $s2, 0xFF
    ROM:8021F428                 lbu     $s1, 0($s0)
    ROM:8021F42C                 addiu   $s0, 1
    ROM:8021F430
    ROM:8021F430 loc_8021F430:                            # CODE XREF: ExpandLzj+278↑j
    ROM:8021F430                 andi    $v0, $s1, 1
    ROM:8021F434                 bnez    $v0, loc_8021F49C
    ROM:8021F438                 li      $a2, 4
    ROM:8021F43C                 srl     $s2, 1
    ROM:8021F440                 bnez    $s2, loc_8021F454
    ROM:8021F444                 srl     $s1, 1
    ROM:8021F448                 li      $s2, 0xFF
    ROM:8021F44C                 lbu     $s1, 0($s0)
    ROM:8021F450                 addiu   $s0, 1
    ROM:8021F454
    ROM:8021F454 loc_8021F454:                            # CODE XREF: ExpandLzj+29C↑j
    ROM:8021F454                 andi    $v0, $s1, 1
    ROM:8021F458                 bnez    $v0, loc_8021F468
    ROM:8021F45C                 li      $a2, 3
    ROM:8021F460                 j       loc_8021F5D0
    ROM:8021F464                 li      $a2, 2
    ROM:8021F468  # ---------------------------------------------------------------------------
    ROM:8021F468
    ROM:8021F468 loc_8021F468:                            # CODE XREF: ExpandLzj+2B4↑j
    ROM:8021F468                 srl     $s2, 1
    ROM:8021F46C                 bnez    $s2, loc_8021F480
    ROM:8021F470                 srl     $s1, 1
    ROM:8021F474                 li      $s2, 0xFF
    ROM:8021F478                 lbu     $s1, 0($s0)
    ROM:8021F47C                 addiu   $s0, 1
    ROM:8021F480
    ROM:8021F480 loc_8021F480:                            # CODE XREF: ExpandLzj+2C8↑j
    ROM:8021F480                 lw      $t0, 0x434($sp)
    ROM:8021F484                 bnez    $t0, loc_8021F4D8
    ROM:8021F488                 andi    $v0, $s1, 1
    ROM:8021F48C                 bnez    $v0, loc_8021F5DC
    ROM:8021F490                 addiu   $a1, $s5, 0x1001
    ROM:8021F494                 j       loc_8021F4C0
    ROM:8021F498                 srl     $s2, 1
    ROM:8021F49C  # ---------------------------------------------------------------------------
    ROM:8021F49C
    ROM:8021F49C loc_8021F49C:                            # CODE XREF: ExpandLzj+290↑j
    ROM:8021F49C                 srl     $s2, 1
    ROM:8021F4A0                 bnez    $s2, loc_8021F4B4
    ROM:8021F4A4                 srl     $s1, 1
    ROM:8021F4A8                 li      $s2, 0xFF
    ROM:8021F4AC                 lbu     $s1, 0($s0)
    ROM:8021F4B0                 addiu   $s0, 1
    ROM:8021F4B4
    ROM:8021F4B4 loc_8021F4B4:                            # CODE XREF: ExpandLzj+2FC↑j
    ROM:8021F4B4                 andi    $v0, $s1, 1
    ROM:8021F4B8                 bnez    $v0, loc_8021F4E8
    ROM:8021F4BC                 srl     $s2, 1
    ROM:8021F4C0
    ROM:8021F4C0 loc_8021F4C0:                            # CODE XREF: ExpandLzj+2F0↑j
    ROM:8021F4C0                 bnez    $s2, loc_8021F4D4
    ROM:8021F4C4                 srl     $s1, 1
    ROM:8021F4C8                 li      $s2, 0xFF
    ROM:8021F4CC                 lbu     $s1, 0($s0)
    ROM:8021F4D0                 addiu   $s0, 1
    ROM:8021F4D4
    ROM:8021F4D4 loc_8021F4D4:                            # CODE XREF: ExpandLzj:loc_8021F4C0↑j
    ROM:8021F4D4                 andi    $v0, $s1, 1
    ROM:8021F4D8
    ROM:8021F4D8 loc_8021F4D8:                            # CODE XREF: ExpandLzj+2E0↑j
    ROM:8021F4D8                 beqz    $v0, loc_8021F5D0
    ROM:8021F4DC                 addiu   $a1, $s5, 1
    ROM:8021F4E0                 j       loc_8021F674
    ROM:8021F4E4                 li      $a0, 0xC
    ROM:8021F4E8  # ---------------------------------------------------------------------------
    ROM:8021F4E8
    ROM:8021F4E8 loc_8021F4E8:                            # CODE XREF: ExpandLzj+314↑j
    ROM:8021F4E8                 bnez    $s2, loc_8021F4FC
    ROM:8021F4EC                 srl     $s1, 1
    ROM:8021F4F0                 li      $s2, 0xFF
    ROM:8021F4F4                 lbu     $s1, 0($s0)
    ROM:8021F4F8                 addiu   $s0, 1
    ROM:8021F4FC
    ROM:8021F4FC loc_8021F4FC:                            # CODE XREF: ExpandLzj:loc_8021F4E8↑j
    ROM:8021F4FC                 andi    $v0, $s1, 1
    ROM:8021F500                 beqz    $v0, loc_8021F5DC
    ROM:8021F504                 addiu   $a1, $s5, 0x1001
    ROM:8021F508                 j       loc_8021F608
    ROM:8021F50C                 lui     $v0, 1
    ROM:8021F510  # ---------------------------------------------------------------------------
    ROM:8021F510
    ROM:8021F510 loc_8021F510:                            # CODE XREF: ExpandLzj+270↑j
    ROM:8021F510                 bnez    $s2, loc_8021F524
    ROM:8021F514                 srl     $s1, 1
    ROM:8021F518                 li      $s2, 0xFF
    ROM:8021F51C                 lbu     $s1, 0($s0)
    ROM:8021F520                 addiu   $s0, 1
    ROM:8021F524
    ROM:8021F524 loc_8021F524:                            # CODE XREF: ExpandLzj:loc_8021F510↑j
    ROM:8021F524                 andi    $v0, $s1, 1
    ROM:8021F528                 bnez    $v0, loc_8021F580
    ROM:8021F52C                 li      $a2, 5
    ROM:8021F530                 srl     $s2, 1
    ROM:8021F534                 bnez    $s2, loc_8021F548
    ROM:8021F538                 srl     $s1, 1
    ROM:8021F53C                 li      $s2, 0xFF
    ROM:8021F540                 lbu     $s1, 0($s0)
    ROM:8021F544                 addiu   $s0, 1
    ROM:8021F548
    ROM:8021F548 loc_8021F548:                            # CODE XREF: ExpandLzj+390↑j
    ROM:8021F548                 andi    $v0, $s1, 1
    ROM:8021F54C                 bnezl   $v0, loc_8021F554
    ROM:8021F550                 li      $a2, 7
    ROM:8021F554
    ROM:8021F554 loc_8021F554:                            # CODE XREF: ExpandLzj+3A8↑j
    ROM:8021F554                 srl     $s2, 1
    ROM:8021F558                 bnez    $s2, loc_8021F56C
    ROM:8021F55C                 srl     $s1, 1
    ROM:8021F560                 li      $s2, 0xFF
    ROM:8021F564                 lbu     $s1, 0($s0)
    ROM:8021F568                 addiu   $s0, 1
    ROM:8021F56C
    ROM:8021F56C loc_8021F56C:                            # CODE XREF: ExpandLzj+3B4↑j
    ROM:8021F56C                 andi    $v0, $s1, 1
    ROM:8021F570                 bnezl   $v0, loc_8021F58C
    ROM:8021F574                 addiu   $a2, 1
    ROM:8021F578                 j       loc_8021F590
    ROM:8021F57C                 srl     $s2, 1
    ROM:8021F580  # ---------------------------------------------------------------------------
    ROM:8021F580
    ROM:8021F580 loc_8021F580:                            # CODE XREF: ExpandLzj+384↑j
    ROM:8021F580                 lbu     $v0, 0($s0)
    ROM:8021F584                 addiu   $s0, 1
    ROM:8021F588                 addiu   $a2, $v0, 9
    ROM:8021F58C
    ROM:8021F58C loc_8021F58C:                            # CODE XREF: ExpandLzj+3CC↑j
    ROM:8021F58C                 srl     $s2, 1
    ROM:8021F590
    ROM:8021F590 loc_8021F590:                            # CODE XREF: ExpandLzj+3D4↑j
    ROM:8021F590                 bnez    $s2, loc_8021F5A4
    ROM:8021F594                 srl     $s1, 1
    ROM:8021F598                 li      $s2, 0xFF
    ROM:8021F59C                 lbu     $s1, 0($s0)
    ROM:8021F5A0                 addiu   $s0, 1
    ROM:8021F5A4
    ROM:8021F5A4 loc_8021F5A4:                            # CODE XREF: ExpandLzj:loc_8021F590↑j
    ROM:8021F5A4                 andi    $v0, $s1, 1
    ROM:8021F5A8                 bnez    $v0, loc_8021F5E4
    ROM:8021F5AC                 srl     $s2, 1
    ROM:8021F5B0                 bnez    $s2, loc_8021F5C4
    ROM:8021F5B4                 srl     $s1, 1
    ROM:8021F5B8                 li      $s2, 0xFF
    ROM:8021F5BC                 lbu     $s1, 0($s0)
    ROM:8021F5C0                 addiu   $s0, 1
    ROM:8021F5C4
    ROM:8021F5C4 loc_8021F5C4:                            # CODE XREF: ExpandLzj+40C↑j
    ROM:8021F5C4                 andi    $v0, $s1, 1
    ROM:8021F5C8                 bnez    $v0, loc_8021F5DC
    ROM:8021F5CC                 addiu   $a1, $s5, 0x1001
    ROM:8021F5D0
    ROM:8021F5D0 loc_8021F5D0:                            # CODE XREF: ExpandLzj+2BC↑j
    ROM:8021F5D0                                          # ExpandLzj:loc_8021F4D8↑j
    ROM:8021F5D0                 li      $a1, 1
    ROM:8021F5D4                 j       loc_8021F674
    ROM:8021F5D8                 li      $a0, 8
    ROM:8021F5DC  # ---------------------------------------------------------------------------
    ROM:8021F5DC
    ROM:8021F5DC loc_8021F5DC:                            # CODE XREF: ExpandLzj+2E8↑j
    ROM:8021F5DC                                          # ExpandLzj+35C↑j ...
    ROM:8021F5DC                 j       loc_8021F674
    ROM:8021F5E0                 li      $a0, 0x10
    ROM:8021F5E4  # ---------------------------------------------------------------------------
    ROM:8021F5E4
    ROM:8021F5E4 loc_8021F5E4:                            # CODE XREF: ExpandLzj+404↑j
    ROM:8021F5E4                 bnez    $s2, loc_8021F5F8
    ROM:8021F5E8                 srl     $s1, 1
    ROM:8021F5EC                 li      $s2, 0xFF
    ROM:8021F5F0                 lbu     $s1, 0($s0)
    ROM:8021F5F4                 addiu   $s0, 1
    ROM:8021F5F8
    ROM:8021F5F8 loc_8021F5F8:                            # CODE XREF: ExpandLzj:loc_8021F5E4↑j
    ROM:8021F5F8                 andi    $v0, $s1, 1
    ROM:8021F5FC                 bnez    $v0, loc_8021F618
    ROM:8021F600                 addiu   $a1, $s5, 1
    ROM:8021F604                 lui     $v0, 1
    ROM:8021F608
    ROM:8021F608 loc_8021F608:                            # CODE XREF: ExpandLzj+364↑j
    ROM:8021F608                 ori     $v0, 0x1001
    ROM:8021F60C                 addu    $a1, $s5, $v0
    ROM:8021F610                 j       loc_8021F674
    ROM:8021F614                 li      $a0, 0x14
    ROM:8021F618  # ---------------------------------------------------------------------------
    ROM:8021F618
    ROM:8021F618 loc_8021F618:                            # CODE XREF: ExpandLzj+458↑j
    ROM:8021F618                 lw      $t0, 0x434($sp)
    ROM:8021F61C                 li      $v0, 2
    ROM:8021F620                 bne     $t0, $v0, loc_8021F644
    ROM:8021F624                 li      $a0, 0xC
    ROM:8021F628                 lui     $v1, 0x11
    ROM:8021F62C                 lw      $t0, 0x41C($sp)
    ROM:8021F630                 li      $v1, 0x111001
    ROM:8021F634                 subu    $v0, $s3, $t0
    ROM:8021F638                 slt     $v1, $v0
    ROM:8021F63C                 beqz    $v1, loc_8021F678
    ROM:8021F640                 li      $v0, 0xC
    ROM:8021F644
    ROM:8021F644 loc_8021F644:                            # CODE XREF: ExpandLzj+47C↑j
    ROM:8021F644                 srl     $s2, 1
    ROM:8021F648                 bnez    $s2, loc_8021F65C
    ROM:8021F64C                 srl     $s1, 1
    ROM:8021F650                 li      $s2, 0xFF
    ROM:8021F654                 lbu     $s1, 0($s0)
    ROM:8021F658                 addiu   $s0, 1
    ROM:8021F65C
    ROM:8021F65C loc_8021F65C:                            # CODE XREF: ExpandLzj+4A4↑j
    ROM:8021F65C                 andi    $v0, $s1, 1
    ROM:8021F660                 beqz    $v0, loc_8021F674
    ROM:8021F664                 lui     $v0, 0x11
    ROM:8021F668                 li      $v0, 0x111001
    ROM:8021F66C                 addu    $a1, $s5, $v0
    ROM:8021F670                 li      $a0, 0x17
    ROM:8021F674
    ROM:8021F674 loc_8021F674:                            # CODE XREF: ExpandLzj+33C↑j
    ROM:8021F674                                          # ExpandLzj+430↑j ...
    ROM:8021F674                 li      $v0, 0xC
    ROM:8021F678
    ROM:8021F678 loc_8021F678:                            # CODE XREF: ExpandLzj+498↑j
    ROM:8021F678                 bne     $a0, $v0, loc_8021F6C8
    ROM:8021F67C                 move    $v1, $zero
    ROM:8021F680                 lw      $t0, 0x434($sp)
    ROM:8021F684                 li      $v0, 2
    ROM:8021F688                 bnel    $t0, $v0, loc_8021F6CC
    ROM:8021F68C                 srl     $s2, 1
    ROM:8021F690
    ROM:8021F690 loc_8021F690:                            # CODE XREF: ExpandLzj+514↓j
    ROM:8021F690                 srl     $s2, 1
    ROM:8021F694                 bnez    $s2, loc_8021F6A8
    ROM:8021F698                 srl     $s1, 1
    ROM:8021F69C                 li      $s2, 0xFF
    ROM:8021F6A0                 lbu     $s1, 0($s0)
    ROM:8021F6A4                 addiu   $s0, 1
    ROM:8021F6A8
    ROM:8021F6A8 loc_8021F6A8:                            # CODE XREF: ExpandLzj+4F0↑j
    ROM:8021F6A8                 sll     $v1, 1
    ROM:8021F6AC                 andi    $v0, $s1, 1
    ROM:8021F6B0                 addiu   $a0, -1
    ROM:8021F6B4                 li      $t0, 8
    ROM:8021F6B8                 bne     $a0, $t0, loc_8021F690
    ROM:8021F6BC                 addu    $v1, $v0
    ROM:8021F6C0                 beqz    $v1, loc_8021F6FC
    ROM:8021F6C4                 nop
    ROM:8021F6C8
    ROM:8021F6C8 loc_8021F6C8:                            # CODE XREF: ExpandLzj:loc_8021F678↑j
    ROM:8021F6C8                                          # ExpandLzj+548↓j
    ROM:8021F6C8                 srl     $s2, 1
    ROM:8021F6CC
    ROM:8021F6CC loc_8021F6CC:                            # CODE XREF: ExpandLzj+4E4↑j
    ROM:8021F6CC                 bnez    $s2, loc_8021F6E0
    ROM:8021F6D0                 srl     $s1, 1
    ROM:8021F6D4                 li      $s2, 0xFF
    ROM:8021F6D8                 lbu     $s1, 0($s0)
    ROM:8021F6DC                 addiu   $s0, 1
    ROM:8021F6E0
    ROM:8021F6E0 loc_8021F6E0:                            # CODE XREF: ExpandLzj:loc_8021F6CC↑j
    ROM:8021F6E0                 sll     $v1, 1
    ROM:8021F6E4                 andi    $v0, $s1, 1
    ROM:8021F6E8                 addiu   $a0, -1
    ROM:8021F6EC                 bnez    $a0, loc_8021F6C8
    ROM:8021F6F0                 addu    $v1, $v0
    ROM:8021F6F4                 addu    $a1, $v1
    ROM:8021F6F8                 sw      $a1, 0x42C($sp)
    ROM:8021F6FC
    ROM:8021F6FC loc_8021F6FC:                            # CODE XREF: ExpandLzj+51C↑j
    ROM:8021F6FC                 lw      $t0, 0x42C($sp)
    ROM:8021F700                 subu    $v1, $s3, $t0
    ROM:8021F704                 lw      $t0, 0x424($sp)
    ROM:8021F708                 addu    $v0, $v1, $a2
    ROM:8021F70C                 sltu    $v0, $t0, $v0
    ROM:8021F710                 bnezl   $v0, loc_8021F74C
    ROM:8021F714                 subu    $a2, $t0, $v1
    ROM:8021F718                 lw      $t0, 0x41C($sp)
    ROM:8021F71C                 sltu    $v0, $v1, $t0
    ROM:8021F720                 beqz    $v0, loc_8021F74C
    ROM:8021F724                 nop
    ROM:8021F728                 lui     $a0, 0x8038
    ROM:8021F72C                 jal     DisplayMessage
    ROM:8021F730                 la      $a0, 0x80386348  # "Compression format error!"
    ROM:8021F734                 lui     $a0, 0x8038
    ROM:8021F738                 jal     DisplayMessage
    ROM:8021F73C                 la      $a0, asc_80385E9C  # "\n"
    ROM:8021F740                 lw      $t0, 0x41C($sp)
    ROM:8021F744                 j       loc_8021F778
    ROM:8021F748                 subu    $v0, $s3, $t0
    ROM:8021F74C  # ---------------------------------------------------------------------------
    ROM:8021F74C
    ROM:8021F74C loc_8021F74C:                            # CODE XREF: ExpandLzj+56C↑j
    ROM:8021F74C                                          # ExpandLzj+57C↑j ...
    ROM:8021F74C                 lbu     $v0, 0($v1)
    ROM:8021F750                 addiu   $v1, 1
    ROM:8021F754                 addiu   $a2, -1
    ROM:8021F758                 sb      $v0, 0($s3)
    ROM:8021F75C                 bnez    $a2, loc_8021F74C
    ROM:8021F760                 addiu   $s3, 1
    ROM:8021F764
    ROM:8021F764 loc_8021F764:                            # CODE XREF: ExpandLzj+178↑j
    ROM:8021F764                                          # ExpandLzj+180↑j ...
    ROM:8021F764                 lw      $t0, 0x424($sp)
    ROM:8021F768                 sltu    $v0, $s3, $t0
    ROM:8021F76C                 bnez    $v0, loc_8021F2A8
    ROM:8021F770                 addiu   $v0, $s0, 4
    ROM:8021F774                 move    $v0, $fp
    ROM:8021F778
    ROM:8021F778 loc_8021F778:                            # CODE XREF: ExpandLzj+8C↑j
    ROM:8021F778                                          # ExpandLzj+5A0↑j
    ROM:8021F778                 lw      $ra, 0x45C($sp)
    ROM:8021F77C                 lw      $fp, 0x458($sp)
    ROM:8021F780                 lw      $s7, 0x454($sp)
    ROM:8021F784                 lw      $s6, 0x450($sp)
    ROM:8021F788                 lw      $s5, 0x44C($sp)
    ROM:8021F78C                 lw      $s4, 0x448($sp)
    ROM:8021F790                 lw      $s3, 0x444($sp)
    ROM:8021F794                 lw      $s2, 0x440($sp)
    ROM:8021F798                 lw      $s1, 0x43C($sp)
    ROM:8021F79C                 lw      $s0, 0x438($sp)
    ROM:8021F7A0                 jr      $ra
    ROM:8021F7A4                 addiu   $sp, 0x460
    ROM:8021F7A4  # End of function ExpandLzj
    """
