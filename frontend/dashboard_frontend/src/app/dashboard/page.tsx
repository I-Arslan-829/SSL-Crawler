import Card from "../../components/Card";
import { fetchOverview } from "@/components/api";
import DonutChart from "../../components/DonutChart";
export default async function OverviewPage() {
  let data;
  try {
    data = await fetchOverview();
  } catch (error) {
    return (
      <div className="text-red-500 font-bold text-xl">
        Failed to fetch overview data.
      </div>
    );
  }

  const summary = data.summary;

  const chartLabels = [
  "Active Certificates",
  "Expiring Soon",
  "Expired Certificates"
];
const chartData = [
  summary.active_certificates,
  summary.expiring_soon,
  summary.expired_certificates,
];
const chartColors = ["#3d60b0ff", "#e8a200ff", "#EF476F"]; // Tuned for your palette

  return (
    <div className="h-full w-full flex flex-col items-center">
     
      <div className=" w-full flex flex-wrap gap-10 justify-center mb-8">
        <Card
          title="Total Certificates"
          value={summary.total_certificates}
          className="w-onethird h-32 hover:bg-navButtonHoverLight dark:hover:bg-navButtonHoverDark"
        />
        <Card
          title="Active Certificates"
          value={summary.active_certificates}
          className="w-onethird h-32 hover:bg-navButtonHoverLight dark:hover:bg-navButtonHoverDark"
        />
        <Card
          title="Expired Certificates"
          value={summary.expired_certificates}
          className="w-onethird h-32 hover:bg-navButtonHoverLight dark:hover:bg-navButtonHoverDark"
        />
        <Card
          title="Expiring Soon"
          value={summary.expiring_soon}
          className="w-onethird h-32 hover:bg-navButtonHoverLight dark:hover:bg-navButtonHoverDark"
        />
        <Card
          title="Unique Domains"
          value={summary.unique_domains_count}
          className="w-onethird h-32 hover:bg-navButtonHoverLight dark:hover:bg-navButtonHoverDark"
        />
        <Card
          title="Unique Issuers"
          value={summary.unique_issuers_count}
          className="w-onethird h-32 hover:bg-navButtonHoverLight dark:hover:bg-navButtonHoverDark"
        />
        {/* <Card
          title="Validation Levels"
          value={Object.entries(summary.validation_levels).map(([k, v]) => `${k}: ${v}`).join(", ")}
          className="w-[47%] h-32 text-sm"
        /> */}
      </div>
      {/* Table card below: */}
      {/* <Card
        title="Show Certificates Table"
        value={summary.total_certificates + " Rows"}
        className="w-full max-w-5xl h-16"
        onClick={() => alert("Table view not developed yet!")}
      /> */}
        <Card
          title="Certificate Status Distribution"
          value={
            <DonutChart
              data={chartData}
              labels={chartLabels}
              colors={chartColors}
            />
          }
          className="w-[30%] h-[80%] flex items-center justify-between"
        />
    </div>
  );
}
