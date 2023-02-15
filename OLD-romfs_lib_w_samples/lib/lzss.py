import ctypes

class lzss():
    """
    ROM:804A8080 ExpandLzss:                              # CODE XREF: ROM:8044010C↑p
    ROM:804A8080                                          # ReadBrowserStorage+27C↑p ...
    ROM:804A8080                 move    $t2, $a1
    ROM:804A8084                 beqz    $a3, locret_804A8134
    ROM:804A8088                 move    $t1, $zero
    ROM:804A808C                 srl     $t1, 1
    ROM:804A8090
    ROM:804A8090 loc_804A8090:                            # CODE XREF: ExpandLzss+AC↓j
    ROM:804A8090                 andi    $v0, $t1, 0x100
    ROM:804A8094                 bnez    $v0, loc_804A80AC
    ROM:804A8098                 andi    $v0, $t1, 1
    ROM:804A809C                 lbu     $v0, 0($a0)
    ROM:804A80A0                 addiu   $a0, 1
    ROM:804A80A4                 ori     $t1, $v0, 0xFF00
    ROM:804A80A8                 andi    $v0, $t1, 1
    ROM:804A80AC
    ROM:804A80AC loc_804A80AC:                            # CODE XREF: ExpandLzss+14↑j
    ROM:804A80AC                 beqzl   $v0, loc_804A80C8
    ROM:804A80B0                 lbu     $t0, 0($a0)
    ROM:804A80B4                 lbu     $v0, 0($a0)
    ROM:804A80B8                 addiu   $a0, 1
    ROM:804A80BC                 sb      $v0, 0($a1)
    ROM:804A80C0                 j       loc_804A8124
    ROM:804A80C4                 addiu   $a1, 1
    ROM:804A80C8  # ---------------------------------------------------------------------------
    ROM:804A80C8
    ROM:804A80C8 loc_804A80C8:                            # CODE XREF: ExpandLzss:loc_804A80AC↑j
    ROM:804A80C8                 addiu   $a0, 1
    ROM:804A80CC                 lbu     $a2, 0($a0)
    ROM:804A80D0                 addiu   $a0, 1
    ROM:804A80D4                 andi    $v1, $a2, 0xF0
    ROM:804A80D8                 andi    $v0, $a2, 0xF
    ROM:804A80DC                 sll     $v1, 4
    ROM:804A80E0                 addiu   $a2, $v0, 2
    ROM:804A80E4                 or      $t0, $v1
    ROM:804A80E8                 slti    $v0, $a2, 0
    ROM:804A80EC                 bnez    $v0, loc_804A8124
    ROM:804A80F0                 move    $v1, $zero
    ROM:804A80F4                 subu    $v0, $a1, $t2
    ROM:804A80F8
    ROM:804A80F8 loc_804A80F8:                            # CODE XREF: ExpandLzss+9C↓j
    ROM:804A80F8                 sltu    $v0, $a3
    ROM:804A80FC                 beqz    $v0, loc_804A8114
    ROM:804A8100                 addiu   $v0, $t0, 1
    ROM:804A8104                 subu    $v0, $a1, $v0
    ROM:804A8108                 lbu     $v0, 0($v0)
    ROM:804A810C                 sb      $v0, 0($a1)
    ROM:804A8110                 addiu   $a1, 1
    ROM:804A8114
    ROM:804A8114 loc_804A8114:                            # CODE XREF: ExpandLzss+7C↑j
    ROM:804A8114                 addiu   $v1, 1
    ROM:804A8118                 slt     $v0, $a2, $v1
    ROM:804A811C                 beqz    $v0, loc_804A80F8
    ROM:804A8120                 subu    $v0, $a1, $t2
    ROM:804A8124
    ROM:804A8124 loc_804A8124:                            # CODE XREF: ExpandLzss+40↑j
    ROM:804A8124                                          # ExpandLzss+6C↑j
    ROM:804A8124                 subu    $v0, $a1, $t2
    ROM:804A8128                 sltu    $v0, $a3
    ROM:804A812C                 bnez    $v0, loc_804A8090
    ROM:804A8130                 srl     $t1, 1
    ROM:804A8134
    ROM:804A8134 locret_804A8134:                         # CODE XREF: ExpandLzss+4↑j
    ROM:804A8134                 jr      $ra
    ROM:804A8138                 subu    $v0, $a1, $t2
    ROM:804A8138  # End of function ExpandLzss
    """
    def ExpandLzss(data, uncompressed_size = 0, flags_start = 0x0000):
        compressed_size = len(data)

        if uncompressed_size == 0:
            uncompressed_size = compressed_size * 2

        uncompressed_data = bytearray(uncompressed_size + 0x08)

        flags = flags_start
        i = 0
        r = 0

        def _add_byte(byte):
            nonlocal r
            uncompressed_data[r] = byte
            r += 1

        while i < compressed_size:
            if (flags & 0x100) == 0:
                flags = ctypes.c_uint32(data[i]).value | 0xFF00
                i += 1

            byte = ctypes.c_uint32(data[i]).value
            if (flags & 0x01) == 0x01:
                _add_byte(byte)
            else:
                i += 1
                next_byte = ctypes.c_uint32(data[i]).value

                m = ((next_byte & 0xF0) << 4) | byte

                for ii in range((next_byte & 0x0F) + 3):
                    _add_byte(uncompressed_data[r - (m + 1)])

            flags >>= 1
            i += 1

            if r >= uncompressed_size:
                break

        return uncompressed_data[0:r]