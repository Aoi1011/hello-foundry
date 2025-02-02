import typing

from solders.pubkey import Pubkey

from restakingpy.accounts.core.slot_toggle import SlotToggle

class NcnVaultTicket:
    """
    This ticket represents the relationship between an NCN and a Vault. It is created by the NCN to opt in to work with a Vault.

    ...

    Attributes
    ----------
    ncn : Pubkey
        The NCN
    
    vault : Pubkey
        The vault account

    index : int
        The index of NcnVaultTicket

    state : SlotToggle
        The state of NcnVaultTicket ()

    bump : int
        The bump seed for the PDA


    Methods
    -------
    deserialize(data: bytes)
        Deserialize the account data to NcnVaultTicket struct

    seeds(ncn: Pubkey, vault: Pubkey):
        Returns the seeds for the PDA

    find_program_address(program_id: Pubkey, ncn: Pubkey, vault: Pubkey):
        Find the program address for the NcnVaultTicket account
    """

    discriminator: typing.ClassVar = 6

    ncn: Pubkey
    vault:Pubkey

    index: int
    state: SlotToggle
    bump: int

    # Initialize a NcnVaultTicket instance with required attributes
    def __init__(self, ncn: Pubkey, vault: Pubkey, index: int, state: SlotToggle, bump: int):
        self.ncn = ncn
        self.vault = vault
        self.index = index
        self.state = state
        self.bump = bump

    # Display NcnVaultTicket
    def __str__(self):
        return (
            f"NcnVaultTicket(\n"
            f"  ncn={self.ncn},\n"
            f"  vault={self.vault},\n"
            f"  index={self.index},\n"
            f"  state={self.state},\n"
            f"  bump={self.bump},\n"
            f")"
        )

    @staticmethod
    def deserialize(data: bytes) -> "NcnVaultTicket":
        """Deserializes bytes into a NcnVaultTicket instance."""
        
        # Define offsets for each field
        offset = 0
        offset += 8

        # NCN
        ncn = Pubkey.from_bytes(data[offset:offset + 32])
        offset += 32

        # Vault
        vault = Pubkey.from_bytes(data[offset:offset + 32])
        offset += 32

        # Index
        index = int.from_bytes(data[offset:offset + 8], byteorder='little')
        offset += 8
        
        # State
        state = SlotToggle.deserialize(data[offset:offset + 8 + 8 + 32])
        offset += 8 + 8 + 32

        # Bump
        bump = int.from_bytes(data[offset:offset + 1])

        # Return a new Config instance with the deserialized data
        return NcnVaultTicket(
            ncn,
            vault,
            index,
            state,
            bump
        )

    @staticmethod
    def seeds(ncn: Pubkey, vault: Pubkey) -> typing.List[bytes]:
        """Return the seeds used for generating PDA."""
        return [b"ncn_vault_ticket", bytes(ncn), bytes(vault)]
    
    @staticmethod
    def find_program_address(program_id: Pubkey, ncn: Pubkey, vault: Pubkey) -> typing.Tuple[Pubkey, int, typing.List[bytes]]:
        """Finds the program-derived address (PDA) for the given seeds and program ID."""
        seeds = NcnVaultTicket.seeds(ncn, vault)
        
        # Compute PDA and bump using seeds (requires solders Pubkey functionality)
        pda, bump = Pubkey.find_program_address(seeds, program_id)
        
        return pda, bump, seeds
