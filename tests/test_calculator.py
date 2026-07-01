import pytest
from core.calculator import quality_bonus, total_chance, total_chance_from_modules, distribute, calculate_with_recycling


class TestQualityBonus:
    def test_qm1_normal(self):
        assert quality_bonus(1, 1) == 0.01

    def test_qm1_legendary(self):
        assert quality_bonus(1, 5) == 0.025

    def test_qm2_normal(self):
        assert quality_bonus(2, 1) == 0.02

    def test_qm3_rare(self):
        assert quality_bonus(3, 3) == 0.039

    def test_invalid_tier(self):
        with pytest.raises(ValueError):
            quality_bonus(4, 1)

    def test_invalid_quality(self):
        with pytest.raises(ValueError):
            quality_bonus(1, 6)


class TestTotalChance:
    def test_zero_modules(self):
        assert total_chance(0, 3, 1) == 0.0

    def test_one_module(self):
        assert total_chance(1, 3, 1) == 0.025

    def test_four_qm3_normal(self):
        assert total_chance(4, 3, 1) == 0.10

    def test_capped_at_100(self):
        # 40 modules of QM3 Normal = 40 * 0.025 = 1.0
        assert total_chance(40, 3, 1) == 1.0
        # exceed should still be 1.0
        assert total_chance(50, 3, 1) == 1.0

    def test_negative_count(self):
        with pytest.raises(ValueError):
            total_chance(-1, 1, 1)

    def test_zero_count_all_tiers(self):
        for tier in [1, 2, 3]:
            for quality in [1, 5]:
                assert total_chance(0, tier, quality) == 0.0

    def test_cap_intermediate(self):
        # 50 QM1 normal = 50 * 0.01 = 0.5 → not capped
        assert abs(total_chance(50, 1, 1) - 0.5) < 1e-10
        # 150 QM1 normal = 150 * 0.01 = 1.5 → capped at 1.0
        assert total_chance(150, 1, 1) == 1.0


class TestTotalChanceFromModules:
    def test_empty_list(self):
        assert total_chance_from_modules([]) == 0.0

    def test_mixed_slots(self):
        result = total_chance_from_modules([(3, 5), (3, 5), None, (1, 1)])
        expected = 0.062 + 0.062 + 0.01
        assert abs(result - expected) < 1e-10

    def test_none_slots_ignored(self):
        result = total_chance_from_modules([None, (2, 3), None, None])
        assert abs(result - 0.032) < 1e-10

    def test_equivalent_to_old_api(self):
        old = total_chance(4, 3, 1)
        new = total_chance_from_modules([(3, 1)] * 4)
        assert abs(old - new) < 1e-10

    def test_too_many_slots(self):
        with pytest.raises(ValueError):
            total_chance_from_modules([(1, 1)] * 10)


class TestDistribute:
    def test_zero_chance(self):
        result = distribute(1, 0.0, 60.0, 5)
        assert result[1] == (1.0, 60.0)
        for level in range(2, 6):
            assert result[level] == (0.0, 0.0)

    def test_max_equals_start(self):
        result = distribute(3, 0.5, 100.0, 3)
        assert result[3] == (1.0, 100.0)
        assert len(result) == 1

    def test_sum_is_one(self):
        result = distribute(1, 0.1, 60.0, 5)
        total = sum(share for share, _ in result.values())
        assert abs(total - 1.0) < 1e-10

    def test_sum_with_various_chances(self):
        for chance in [0.0, 0.25, 0.5, 0.75, 1.0]:
            result = distribute(1, chance, 100.0, 5)
            total = sum(share for share, _ in result.values())
            assert abs(total - 1.0) < 1e-10

    def test_start_not_zero(self):
        result = distribute(2, 0.2, 50.0, 5)
        assert 2 in result
        assert 1 not in result

    def test_start_exceeds_max(self):
        with pytest.raises(ValueError):
            distribute(4, 0.1, 60.0, 3)

    def test_items_per_min(self):
        result = distribute(1, 0.0, 60.0, 5)
        assert result[1][1] == 60.0
        for level in range(2, 6):
            assert result[level][1] == 0.0

    def test_cascade_limited_by_max(self):
        result = distribute(1, 1.0, 100.0, 2)
        # With 100% chance, all should go to level 2 or stay at 1
        # P(at 1) = 0
        # P(at 2) = 1.0 (cascade stops at max)
        assert abs(result[1][0]) < 1e-10
        assert abs(result[2][0] - 1.0) < 1e-10

    def test_items_per_min_match_share_times_rate(self):
        result = distribute(1, 0.25, 200.0, 5)
        for level in range(1, 6):
            share, items = result[level]
            assert abs(items - share * 200.0) < 1e-10

    def test_specific_distribution(self):
        # With Q=0.1 from start_level=1, max_unlocked=5:
        # P(1) = 0.9
        # P(2) = 0.1 * 0.9 = 0.09
        # P(3) = 0.1 * 0.09 = 0.009
        # P(4) = 0.1 * 0.009 = 0.0009
        # P(5) = 0.1 * 0.0009 = 0.00009 + overflow 0.00001 = 0.0001
        # Actually let me use the formula:
        # P(1) = 1 - Q = 0.9
        # P(2) = Q * 0.9 = 0.09
        # P(3) = Q * 0.09 = 0.009
        # P(4) = Q * 0.009 = 0.0009
        # P(5) = Q * 0.1^4 / 0.9... actually P(5) = Q * 0.1^(m-1) where m=4
        # P(5) = 0.1 * 0.1^3 = 0.0001
        result = distribute(1, 0.1, 100.0, 5)
        assert abs(result[1][0] - 0.9) < 1e-10
        assert abs(result[2][0] - 0.09) < 1e-10
        assert abs(result[3][0] - 0.009) < 1e-10
        assert abs(result[4][0] - 0.0009) < 1e-10
        assert abs(result[5][0] - 0.0001) < 1e-10


class TestRecycling:
    def test_threshold_normal_recycles_level1(self):
        result = calculate_with_recycling(
            base_input=60.0, start_level=1,
            Q_prod=0.1, Q_rec=0.0,
            recycle_threshold=1, max_unlocked_level=5,
        )
        single = distribute(1, 0.1, 60.0, 5)
        # Level 1 items are recycled (1 <= 1), so they never exit
        assert abs(result[1]) < 1e-9
        # Recycled material produces more output at levels 2+
        for level in range(2, 6):
            assert result[level] > single[level][1]

    def test_qrec_zero_25pct_return(self):
        result = calculate_with_recycling(
            base_input=100.0, start_level=1,
            Q_prod=0.0, Q_rec=0.0,
            recycle_threshold=2, max_unlocked_level=5,
        )
        # All output stays at level 1, gets recycled
        # Series: 100 + 25 + 6.25 + ... = 100 * 4/3 = 133.33...
        # But nothing exits because level 1 < threshold=2
        for level in range(2, 6):
            assert result[level] == 0.0

    def test_threshold_uncommon_recycles_up_to_uncommon(self):
        result = calculate_with_recycling(
            base_input=100.0, start_level=1,
            Q_prod=0.2, Q_rec=0.0,
            recycle_threshold=2, max_unlocked_level=5,
        )
        # Items at level 1 and 2 are recycled (<=2), levels 3+ exit
        single = distribute(1, 0.2, 100.0, 5)
        # Level 1 and 2 should be 0 (recycled)
        assert abs(result[1]) < 1e-9
        assert abs(result[2]) < 1e-9
        # Levels 3+ accumulate recycled material, so > single pass
        for level in range(3, 6):
            assert result[level] > single[level][1]

    def test_sum_matches_convergence(self):
        result = calculate_with_recycling(
            base_input=60.0, start_level=1,
            Q_prod=0.1, Q_rec=0.0,
            recycle_threshold=2, max_unlocked_level=5,
        )
        # Items at level 2+ exit, level 1 recycled
        # With Q_prod=0.1: level 2+ = 0.1 of each cycle's input
        # Recycler returns 25% of level 1 (90% of input) = 0.225 of input
        # Total processed = 60 / (1 - 0.225) ≈ 77.42
        # Total out = 77.42 * 0.1 ≈ 7.74
        # So total_out should be less than base_input (quality costs quantity)
        total_out = sum(result.values())
        assert total_out < 60.0

    def test_recycling_converges_fast(self):
        result = calculate_with_recycling(
            base_input=1000.0, start_level=1,
            Q_prod=0.25, Q_rec=0.1,
            recycle_threshold=3, max_unlocked_level=5,
        )
        total = sum(result.values())
        assert total > 0
        # All levels should have values >= 0
        for lvl in range(1, 6):
            assert result[lvl] >= 0

    def test_high_threshold_no_exit(self):
        result = calculate_with_recycling(
            base_input=100.0, start_level=1,
            Q_prod=0.0, Q_rec=0.0,
            recycle_threshold=5, max_unlocked_level=5,
        )
        # Everything stays at level 1, threshold=5 means all levels recycled (5 <= 5)
        # With 0 quality, nothing exits (nothing reaches level 5)
        assert result[5] == 0.0

    def test_validation_start_exceeds_max(self):
        with pytest.raises(ValueError):
            calculate_with_recycling(
                base_input=60.0, start_level=4,
                Q_prod=0.1, Q_rec=0.0,
                recycle_threshold=2, max_unlocked_level=3,
            )

    def test_mass_balance_geometric_series(self):
        result = calculate_with_recycling(
            base_input=100.0, start_level=1,
            Q_prod=0.0, Q_rec=0.0,
            recycle_threshold=1, max_unlocked_level=1,
        )
        # Q=0: everything stays at level 1.
        # threshold=1: level 1 recycled.
        # Series: 100 → 25 → 6.25 → ... → 0 after ~20 iterations
        # With max_unlocked=1, threshold=1, never exits, so result[1] = 0
        assert abs(result[1]) < 1e-9

    def test_mass_balance_recycling_ratio(self):
        result = calculate_with_recycling(
            base_input=100.0, start_level=1,
            Q_prod=0.2, Q_rec=0.0,
            recycle_threshold=1, max_unlocked_level=5,
        )
        # Q_prod=0.2, only level 1 recycled (<=1)
        # Each cycle: 80% of processed material stays at lvl1 and gets recycled
        # Recycler returns 25% of that = 20% of processed material
        # Total processed = 100 / (1 - 0.8*0.25) = 100 / 0.8 = 125
        # Total output = 125 * 0.2 = 25 (levels 2-5 combined)
        total_out = sum(result.values())
        assert abs(total_out - 25.0) < 1.0

    def test_recycler_quality_improves_output(self):
        no_q = calculate_with_recycling(
            base_input=100.0, start_level=1,
            Q_prod=0.1, Q_rec=0.0,
            recycle_threshold=2, max_unlocked_level=5,
        )
        with_q = calculate_with_recycling(
            base_input=100.0, start_level=1,
            Q_prod=0.1, Q_rec=0.2,
            recycle_threshold=2, max_unlocked_level=5,
        )
        # With recycler quality, more items should be upgraded to higher levels
        for level in range(2, 6):
            assert with_q[level] >= no_q[level] - 1e-9


class TestRecyclingValidation:
    def test_qprod_gt_1(self):
        with pytest.raises(ValueError):
            calculate_with_recycling(
                base_input=60.0, start_level=1,
                Q_prod=1.1, Q_rec=0.0,
                recycle_threshold=2, max_unlocked_level=5,
            )

    def test_qrec_lt_0(self):
        with pytest.raises(ValueError):
            calculate_with_recycling(
                base_input=60.0, start_level=1,
                Q_prod=0.1, Q_rec=-0.1,
                recycle_threshold=2, max_unlocked_level=5,
            )

    def test_base_input_negative(self):
        with pytest.raises(ValueError):
            calculate_with_recycling(
                base_input=-10.0, start_level=1,
                Q_prod=0.1, Q_rec=0.0,
                recycle_threshold=2, max_unlocked_level=5,
            )

    def test_recycle_threshold_lt_1(self):
        with pytest.raises(ValueError):
            calculate_with_recycling(
                base_input=60.0, start_level=1,
                Q_prod=0.1, Q_rec=0.0,
                recycle_threshold=0, max_unlocked_level=5,
            )

    def test_recycle_threshold_gt_max(self):
        with pytest.raises(ValueError):
            calculate_with_recycling(
                base_input=60.0, start_level=1,
                Q_prod=0.1, Q_rec=0.0,
                recycle_threshold=6, max_unlocked_level=5,
            )

    def test_threshold_equals_max_unlocked_with_qprod_zero(self):
        result = calculate_with_recycling(
            base_input=100.0, start_level=1,
            Q_prod=0.0, Q_rec=0.0,
            recycle_threshold=5, max_unlocked_level=5,
        )
        # All material stays at level 1 and gets recycled (1 <= 5)
        # Since Q_prod=0, nothing upgrades → infinite loop without convergence check
        # Actually: 100% stays at lvl1 → recycled → 25 → 6.25 → ... → 0
        # Final output should be 0 at all levels
        for level in range(1, 6):
            assert result[level] >= 0.0
        total = sum(result.values())
        assert total < 1e-6

    def test_max_iterations_converges(self):
        result = calculate_with_recycling(
            base_input=1e6, start_level=1,
            Q_prod=0.99, Q_rec=0.99,
            recycle_threshold=3, max_unlocked_level=5,
        )
        # Extreme: high quality both sides, large input
        # Should converge to finite values, not infinite loop
        for level in range(1, 6):
            assert result[level] >= 0
        total = sum(result.values())
        assert 0 < total < 1e6
