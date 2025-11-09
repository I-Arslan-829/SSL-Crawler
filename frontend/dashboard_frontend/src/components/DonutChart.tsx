"use client";
import { Doughnut } from "react-chartjs-2";
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js';
import React, { useRef } from "react";

ChartJS.register(ArcElement, Tooltip, Legend);

export default function DonutChart({
  data,
  labels,
  colors,
  onSegmentClick,
}: {
  data: number[];
  labels: string[];
  colors?: string[];
  onSegmentClick?: (label: string, value: number) => void;
}) {
  const chartRef = useRef<any>(null);

  // Make chart itself clickable and hoverable
  const options = {
    plugins: {
      legend: { display: true, position: 'bottom' },
      tooltip: {
        callbacks: {
          label: function(context: any) {
            let label = context.label || "";
            let value = context.parsed || "";
            return `${label}: ${value}`;
          }
        }
      }
    },
    onClick: (evt: any) => {
      if (!onSegmentClick || !chartRef.current) return;
      const points = chartRef.current.getElementsAtEventForMode(
        evt,
        'nearest',
        { intersect: true },
        false
      );
      if (points.length) {
        const { index } = points[0];
        onSegmentClick(labels[index], data[index]);
      }
    }
  };

  const chartData = {
    labels,
    datasets: [
      {
        data,
        backgroundColor: colors || ["#7caf9f", "#f49d6e", "#f5e960"],
        borderWidth: 2,
      },
    ],
  };

 return (
  <div className="w-[100%] h-[100%]     flex items-center justify-center">
    <Doughnut ref={chartRef} data={chartData} options={options} />
  </div>
);
}
