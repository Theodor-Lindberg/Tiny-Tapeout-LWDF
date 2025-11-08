library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.NUMERIC_STD.ALL;

entity tt_um_lwdf_top is
    port (
        ui_in   : in  std_logic_vector(7 downto 0);
        uo_out  : out std_logic_vector(7 downto 0);
        uio_in  : in  std_logic_vector(7 downto 0);
        uio_out : out std_logic_vector(7 downto 0);
        uio_oe  : out std_logic_vector(7 downto 0);
        ena     : in  std_logic;
        clk     : in  std_logic;
        rst_n   : in  std_logic
    );
end tt_um_lwdf_top;

architecture Behavioral of tt_um_lwdf_top is

    component lwdf is
    port (
        clk : in std_logic;
        rst : in std_logic;
        in0_0_in : in std_logic_vector(7 downto 0);
        out0_0_out : out std_logic_vector(7 downto 0)
    );
    end component;

    signal rst : std_logic;

begin

    rst <= not rst_n;
    uio_oe <= "00000000";

    lwdf_inst : lwdf 
    port map(
        clk => clk,
        rst => rst,
        in0_0_in => ui_in,
        out0_0_out => uo_out
    );

end Behavioral;