import math

def solve():
    ip_input = input("Enter the IP address with CIDR notation (e.g., 192.168.10.0/24): ")
    ip_address, prefix = ip_input.split('/')
    prefix = int(prefix)
    octets = list(map(int, ip_address.split('.')))

    # Generate the subnet sizes array
    Subnet_arr = [2 ** i for i in range(32)]

    n = int(input("Number of Subnets: "))
    host_arr = []

    IP_addresses_needed = 0
    for i in range(n):
        subnet_name = chr(65 + i)  # Assigning names A, B, C...
        host_size = int(input(f"Subnet {subnet_name} (number of hosts): "))
        host_arr.append((host_size, subnet_name))
        IP_addresses_needed += host_size + 2  # Add 2 for network and broadcast addresses

    # Sort the host array in descending order by host size
    host_arr.sort(reverse=True, key=lambda x: x[0])

    # Calculate available IP addresses in the given network
    available_ips = 2 ** (32 - prefix)

    if IP_addresses_needed > available_ips:
        print("Subnetting failed")
        print(f"IP addresses needed: {IP_addresses_needed}, Available IP addresses: {available_ips}")
        return

    print("-" * 145)
    print("| HostName | Hosts Size | Network Address   | Mask (Decimal)     | Slash Notation | First IP Address    | Last IP Address     | Broadcast Address   |")
    print("-" * 145)

    current_base = int.from_bytes(octets, byteorder='big') & ((1 << 32) - (1 << (32 - prefix)))

    for host_size, subnet_name in host_arr:
        required_ips = 2 ** math.ceil(math.log2(host_size + 2))

        # Subnet Mask
        new_prefix = 32 - int(math.log2(required_ips))
        subnet_mask = f"/{new_prefix}"

        # Subnet Mask in Decimal Notation
        mask_value = (1 << 32) - (1 << (32 - new_prefix))
        decimal_mask = [
            (mask_value >> 24) & 0xFF,
            (mask_value >> 16) & 0xFF,
            (mask_value >> 8) & 0xFF,
            mask_value & 0xFF,
        ]
        decimal_mask_str = ".".join(map(str, decimal_mask))

        # Network Address
        network_address = [
            (current_base >> 24) & 0xFF,
            (current_base >> 16) & 0xFF,
            (current_base >> 8) & 0xFF,
            current_base & 0xFF,
        ]
        network_address_str = ".".join(map(str, network_address))

        # First IP Address
        first_ip = current_base + 1
        first_ip_str = ".".join(map(str, [
            (first_ip >> 24) & 0xFF,
            (first_ip >> 16) & 0xFF,
            (first_ip >> 8) & 0xFF,
            first_ip & 0xFF,
        ]))

        # Last IP Address and Broadcast Address
        last_ip = current_base + required_ips - 2
        broadcast_ip = current_base + required_ips - 1

        last_ip_str = ".".join(map(str, [
            (last_ip >> 24) & 0xFF,
            (last_ip >> 16) & 0xFF,
            (last_ip >> 8) & 0xFF,
            last_ip & 0xFF,
        ]))

        broadcast_ip_str = ".".join(map(str, [
            (broadcast_ip >> 24) & 0xFF,
            (broadcast_ip >> 16) & 0xFF,
            (broadcast_ip >> 8) & 0xFF,
            broadcast_ip & 0xFF,
        ]))

        print(f"|   {subnet_name}      |    {host_size}      | {network_address_str:<17} | {decimal_mask_str:<18} | {subnet_mask:<13} | {first_ip_str:<18} | {last_ip_str:<18} | {broadcast_ip_str:<18} |")

        # Move base to the next subnet
        current_base += required_ips

if __name__ == "__main__":
    solve()
