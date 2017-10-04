def gen_ip_by_dot(string, dot_pos):
    """generate the ip string based on the array `dot_pos`"""
    return string[:dot_pos[0]] + '.' + string[dot_pos[0]:dot_pos[1]] + '.' + string[dot_pos[1]:dot_pos[2]] + '.' + string[dot_pos[2]:]

dot_poses = []
dot_pos = [0, 0, 0]
def gen_dot_poses(step, be_head, be_three, pos):
    """
    step: 0, 1, 2, 3(finish)
    pos: e.g.
        140112140112
        oo.oo.oo.ooo
        012345678901
        dot_pos = [2, 5, 8]
    """
    global dot_poses
    global dot_pos

    if len(be_three) == 0 or not be_head[0]:
        return

    if step == 3:
        if len(be_three) < 3:
            dot_poses += [list(dot_pos)]
        elif len(be_three) == 3:
            if be_three[0]:
                dot_poses += [list(dot_pos)]
        return

    if len(be_three) > (4 - step) * 3 or len(be_three) < 4 - step:
        return

    dot_pos[step] = pos + 1
    gen_dot_poses(step + 1, be_head[1:], be_three[1:], pos + 1)
    dot_pos[step] = pos + 2
    gen_dot_poses(step + 1, be_head[2:], be_three[2:], pos + 2)
    if be_three[0]:
        dot_pos[step] = pos + 3
        gen_dot_poses(step + 1, be_head[3:], be_three[3:], pos + 3)

def gen_be_head(string):
    be_head = [True] * (len(string))
    for i,_ in enumerate(be_head):
        if string[i] == '0':
            be_head[i] = False
    return be_head

def gen_be_three(string):
    be_three = [False] * (len(string))
    for i in range(len(be_three) - 2):
        if string[i] == '1':
            be_three[i] = True
        elif string[i] == '2':
            if string[i + 1] < '5':
                be_three[i] = True
            elif string[i + 1] == '5' and string[i + 2] < '6':
                be_three[i] = True
    return be_three

def gen_ips(ip_str):
    global dot_poses
    global dot_pos

    dot_poses = []
    dot_pos = [0, 0, 0]

    be_head = gen_be_head(ip_str)
    be_three = gen_be_three(ip_str)
    gen_dot_poses(0, be_head, be_three, 0)

    ips = []
    for dot_pos in dot_poses:
        ips += [gen_ip_by_dot(ip_str, dot_pos)]
    return ips

if __name__ == "__main__":
    ip_str = '12409234'
    print(gen_ips(ip_str))
    ip_str = '12345'
    print(gen_ips(ip_str))
