import React from "react";
import { employees } from "./data";

interface TreeNode {
  id: number;
  name: string;
  title: string;
  manager_id: number | null;
  direct_reports?: TreeNode[];
}

interface TreeProps {
  data: TreeNode[];
}

const TreeNodeComponent: React.FC<{ node: TreeNode }> = ({ node }) => {
  const hasChildren = node.direct_reports && node.direct_reports.length > 0;

  return (
    <div className="tree-node">
      <div className="node-label">
        <span className="node-text">
          {node.name} - {node.title}
        </span>
      </div>
      {hasChildren && (
        <div className="node-children">
          {node.direct_reports?.map((child) => (
            <TreeNodeComponent key={child.id} node={child} />
          ))}
        </div>
      )}
    </div>
  );
};

const Tree: React.FC<TreeProps> = () => {
  return (
    <div className="tree-container">
      {employees.map((node) => (
        <TreeNodeComponent key={node.id} node={node} />
      ))}
    </div>
  );
};

export default Tree;
